/*
 * Competition method 2, which implements Eq. 40 in the lab notes (See
 * paper/supplementary/supp.tex; label eq:J_NM_with_comp)
 */

#include "rd_james.h"

#include <vector>
#include <array>
#include <iostream>

template <class Flt>
class RD_James_comp2 : public RD_James<Flt>
{
public:
    /*!
     * Parameter which controls the strength of diffusion away from
     * axon branching of other TC types.
     */
    alignas(alignof(std::vector<Flt>))
    std::vector<Flt> epsilon;
    //! epsilon / (N-1)
    alignas(alignof(std::vector<Flt>))
    std::vector<Flt> epsilonOverNm1;

    /*!
     * \hat{a}_i. Recomputed for each new i, so doesn't need to be a
     * vector of vectors.
     */
    alignas(alignof(std::vector<Flt>))
    std::vector<Flt> ahat;

    /*!
     * This holds the two components of the gradient field of the
     * scalar value \hat{a}_i(x,t), which is the sum of the branching
     * densities of all axon types except i.
     */
    alignas(alignof(std::array<std::vector<Flt>, 2>))
    std::array<std::vector<Flt>, 2> grad_ahat;

    /*!
     * divergence of \hat{a}_i(x,t).
     */
    alignas(alignof(std::vector<Flt>))
    std::vector<Flt> div_ahat;

    /*!
     * \bar{a}_i - result of processing a_i through a sigmoid.
     */
    //@{
    alignas(alignof(std::vector<Flt>))
    std::vector<Flt> abar;
    alignas(alignof(std::array<std::vector<Flt>, 2>))
    std::array<std::vector<Flt>, 2> grad_abar;
    //@}

    /*!
     * Simple constructor; no arguments. Just calls base constructor
     */
    RD_James_comp2 (void)
        : RD_James<Flt>() {
    }

    /*!
     * Override allocate() and init(), and add a couple of extra
     * resizes.
     */
    //@{
    virtual void allocate (void) {
        RD_James<Flt>::allocate();
        this->resize_vector_variable (this->ahat);
        this->resize_gradient_field (this->grad_ahat);
        this->resize_vector_variable (this->div_ahat);
        this->resize_vector_variable (this->abar);
        this->resize_gradient_field (this->grad_abar);
        // epsilon based competition
        this->resize_vector_param (this->epsilon, this->N);
        this->resize_vector_param (this->epsilonOverNm1, this->N);
    }
    virtual void init (void) {
        RD_James<Flt>::init();
        this->zero_vector_variable (this->ahat);
        this->zero_gradient_field (this->grad_ahat);
        this->zero_vector_variable (this->div_ahat);
        this->zero_vector_variable (this->abar);
        this->zero_gradient_field (this->grad_abar);

        // Set up the competition params
        if (this->N > 0) {
            for (unsigned int i = 0; i < this->N; ++i) {
                this->epsilonOverNm1[i] = this->epsilon[i]/(this->N-1);
            }
        } else {
            this->zero_vector_param (this->epsilonOverNm1, this->N);
        }
    }
    //@}
    /*!
     * Computation methods
     */
    //@{

    /*!
     * This is updated wrt rd_james.h as it has the additional terms
     *
     * Computes the "flux of axonal branches" term, J_i(x) (Eq 4)
     *
     * Inputs: this->g, fa (which is this->a[i] or a q in the RK
     * algorithm), this->D, @a i, the TC type.  Helper functions:
     * spacegrad2D().  Output: this->divJ
     *
     * Stable with dt = 0.0001;
     *
     * In the competition term, it's possible to set \bar{a} equal to either sigmoid
     * transfer function of {a} with SIGMOID_ROLLOFF_FOR_A (which maxes out at 2.0) or a
     * linear transfer function of {a} with a maximum of 2.0 with LINEAR_MAX. Do so when
     * compiling with, e.g. -DLINEAR_MAX. Initially, I thought a transfer function was
     * necessary, but it is not (though use of a transfer function does extend the range
     * of parameters for which this model is stable).
     */
    virtual void compute_divJ (std::vector<Flt>& fa, unsigned int i) {

        // Now prefer if constexpr, but icc doesn't like pragma omp inside an if constexpr.
#ifdef SIGMOID_ROLLOFF_FOR_A
        // Compute \bar{a}_i and its spatial gradient
        Flt h = 2.0; // height parameter for sigmoid
        Flt o = 5.0; // offset
        Flt s = 0.5; // sharpness
#pragma omp parallel for
        for (unsigned int hi=0; hi<this->nhex; ++hi) {
            this->abar[hi] = h / (1 - exp (o - s * fa[hi]));
        }
        this->spacegrad2D (this->abar, this->grad_abar);
#elif defined LINEAR_MAX
        Flt h = 2.0; // Max value for a
#pragma omp parallel for
        for (unsigned int hi=0; hi<this->nhex; ++hi) {
            this->abar[hi] = fa[hi] > h ? h : fa[hi];
        }
        this->spacegrad2D (this->abar, this->grad_abar);
#endif

        // Compute gradient of a_i(x), for use computing the third term, below.
        this->spacegrad2D (fa, this->grad_a[i]);

        // _Five_ terms to compute; see Eq. 17 in methods_notes.pdf. Copy comp3.
#pragma omp parallel for //schedule(static) // This was about 10% faster than schedule(dynamic,50).
        for (unsigned int hi=0; hi<this->nhex; ++hi) {

            // 1. The D Del^2 a_i term. Eq. 18.
            // 1a. Or D Del^2 Sum(a_i) (new)
            // Compute the sum around the neighbours
            Flt thesum = -6 * fa[hi];

            thesum += fa[(HAS_NE(hi)  ? NE(hi)  : hi)];
            thesum += fa[(HAS_NNE(hi) ? NNE(hi) : hi)];
            thesum += fa[(HAS_NNW(hi) ? NNW(hi) : hi)];
            thesum += fa[(HAS_NW(hi)  ? NW(hi)  : hi)];
            thesum += fa[(HAS_NSW(hi) ? NSW(hi) : hi)];
            thesum += fa[(HAS_NSE(hi) ? NSE(hi) : hi)];

            // Multiply sum by 2D/3d^2 to give term1
            Flt term1 = this->twoDover3dd * thesum;
            if (isnan(term1)) {
                std::cerr << "term1 isnan" << std::endl;
                std::cerr << "thesum is " << thesum << " fa[hi=" << hi << "] = " << fa[hi] << std::endl;
                exit (21);
            }

            Flt term1_1 = Flt{0};
#if defined SIGMOID_ROLLOFF_FOR_A || defined LINEAR_MAX
            // Term 1.1 is epsilon/N-1 abar div(ahat)
            term1_1 = this->epsilonOverNm1[i] * abar[hi] * this->div_ahat[hi];
#else
            // Term 1.1 is epsilon/N-1 a div(ahat)
            term1_1 = this->epsilonOverNm1[i] * fa[hi] * this->div_ahat[hi];
#endif

            if (isnan(term1_1)) {
                std::cerr << "term1_1 isnan" << std::endl;
                std::cerr << "fa[hi="<<hi<<"] = " << fa[hi] << ", this->div_ahat[hi] = " << this->div_ahat[hi] << std::endl;
                exit (21);
            }

            Flt term1_2 = Flt{0};
#if defined SIGMOID_ROLLOFF_FOR_A || defined LINEAR_MAX
            // Term 1.2 is F/N-1 grad(ahat) . grad(abar)
            term1_2 = this->epsilonOverNm1[i] * (this->grad_ahat[0][hi] * this->grad_abar[0][hi]
                                                 + this->grad_ahat[1][hi] * this->grad_abar[1][hi]);
#else
            // Term 1.2 is F/N-1 grad(ahat) . grad(a)
            term1_2 = this->epsilonOverNm1[i] * (this->grad_ahat[0][hi] * this->grad_a[i][0][hi]
                                                 + this->grad_ahat[1][hi] * this->grad_a[i][1][hi]);
#endif

            if (isnan(term1_2)) {
                std::cerr << "term1_2 isnan at hi=" << hi << std::endl;
                if (isnan(this->grad_ahat[0][hi])) {
                    std::cerr << "grad_ahat[0][hi] isnan\n";
                }
                if (isnan(this->grad_ahat[1][hi])) {
                    std::cerr << "grad_ahat[1][hi] isnan\n";
                }
                if (isnan(this->grad_abar[0][hi])) {
                    std::cerr << "grad_abar[0][hi] isnan; abar is " << this->abar[hi] << ", neighbouring abars: "
                              << "NE: " << (HAS_NE(hi) ? this->abar[NE(hi)] : -1)
                              << ", NNE: " << (HAS_NNE(hi) ? this->abar[NNE(hi)] : -1)
                              << ", NNW: " << (HAS_NNW(hi) ? this->abar[NNW(hi)] : -1)
                              << ", NW: " << (HAS_NW(hi) ? this->abar[NW(hi)] : -1)
                              << ", NSW: " << (HAS_NSW(hi) ? this->abar[NSW(hi)] : -1)
                              << ", NSE: " << (HAS_NSE(hi) ? this->abar[NSE(hi)] : -1)
                              << "\n";
                }
                if (isnan(this->grad_abar[1][hi])) {
                    std::cerr << "grad_abar[1][hi] isnan; abar is " << this->abar[hi] << "\n";
                }
                exit (21);
            }

            // 2. The (a div(g)) term.
            Flt term2 = 0.0;

            // 3. Third term is this->g . grad a_i. Should not contribute to J, as
            // g(x) decays towards boundary.
            Flt term3 = 0.0;

            for (unsigned int m =0 ; m < this->M; ++m) {
                if (this->stepCount >= this->guidance_time_onset[m]) {
                    // g contributes to term2
                    term2 += fa[hi] * this->divg_over3d[m][i][hi];
                    // and to term3
                    term3 += this->g[m][i][0][hi] * this->grad_a[i][0][hi] + (this->g[m][i][1][hi] * this->grad_a[i][1][hi]);
                }
            }

            // - term1_1/2 or + term1_1/2? It's + in the supp.tex
            this->divJ[i][hi] = term1 + term1_1 + term1_2 - term2 - term3;
        }
    }

    /*!
     * Compute divergence of \hat{a}_i
     */
    void compute_divahat (void) {
#pragma omp parallel for
        for (unsigned int hi=0; hi<this->nhex; ++hi) {
            Flt thesum = -6 * this->ahat[hi];
            thesum += this->ahat[(HAS_NE(hi)  ? NE(hi)  : hi)];
            thesum += this->ahat[(HAS_NNE(hi) ? NNE(hi) : hi)];
            thesum += this->ahat[(HAS_NNW(hi) ? NNW(hi) : hi)];
            thesum += this->ahat[(HAS_NW(hi)  ? NW(hi)  : hi)];
            thesum += this->ahat[(HAS_NSW(hi) ? NSW(hi) : hi)];
            thesum += this->ahat[(HAS_NSE(hi) ? NSE(hi) : hi)];
            this->div_ahat[hi] = this->twoover3dd * thesum;
            if (isnan(this->div_ahat[hi])) {
                std::cerr << "div ahat isnan" << std::endl;
                exit (3);
            }
        }
    }

    /*!
     * integrate_a has some additional code in.
     *
     * Compute the values of a, the branching density
     */
    virtual void integrate_a (void) {

        // 2. Do integration of a (RK in the 1D model). Involves computing axon
        // branching flux.

        // Pre-compute:
        // 1) The intermediate val alpha_c.
        for (unsigned int i=0; i<this->N; ++i) {
#pragma omp parallel for
            for (unsigned int h=0; h<this->nhex; ++h) {
                this->alpha_c[i][h] = this->alpha[i] * this->c[i][h];
            }
        }

        // Runge-Kutta: No OMP here - there are only N(<10) loops, which isn't enough
        // to load the threads up.
        for (unsigned int i=0; i<this->N; ++i) {

            // --- START specific to comp2 method ---
            // Compute "the sum of all a_j for which j!=i"
            this->zero_vector_variable (this->ahat);
            for (unsigned int j=0; j<this->N; ++j) {
                if (j==i) { continue; }
#pragma omp parallel for
                for (unsigned int h=0; h<this->nhex; ++h) {
                    this->ahat[h] += this->a[j][h];
                }
            }
            // 1.1 Compute divergence and gradient of ahat
            this->compute_divahat();
            this->spacegrad2D (this->ahat, this->grad_ahat);
            // --- END specific to comp2 method ---

            // Runge-Kutta integration for A
            std::vector<Flt> qq(this->nhex, 0.0);
            this->compute_divJ (this->a[i], i); // populates divJ[i]

            std::vector<Flt> k1(this->nhex, 0.0);
#pragma omp parallel for
            for (unsigned int h=0; h<this->nhex; ++h) {
                k1[h] = this->divJ[i][h] - this->dc[i][h];
                qq[h] = this->a[i][h] + k1[h] * this->halfdt;
            }

            std::vector<Flt> k2(this->nhex, 0.0);
            this->compute_divJ (qq, i);
#pragma omp parallel for
            for (unsigned int h=0; h<this->nhex; ++h) {
                k2[h] = this->divJ[i][h] - this->dc[i][h];
                qq[h] = this->a[i][h] + k2[h] * this->halfdt;
            }

            std::vector<Flt> k3(this->nhex, 0.0);
            this->compute_divJ (qq, i);
#pragma omp parallel for
            for (unsigned int h=0; h<this->nhex; ++h) {
                k3[h] = this->divJ[i][h] - this->dc[i][h];
                qq[h] = this->a[i][h] + k3[h] * this->dt;
            }

            std::vector<Flt> k4(this->nhex, 0.0);
            this->compute_divJ (qq, i);
#pragma omp parallel for
            for (unsigned int h=0; h<this->nhex; ++h) {
                k4[h] = this->divJ[i][h] - this->dc[i][h];
                this->a[i][h] += (k1[h] + 2.0 * (k2[h] + k3[h]) + k4[h]) * this->sixthdt;
            }
#if 0
            // Find max and min of this->a[i] and report when the max of maxes gets maxer...
            pair<Flt, Flt> mm = morph::MathAlgo::maxmin (this->a[i]);
#endif

#if 0
            // Do any necessary computation which involves summing a here
            this->sum_a_computation (i);

            // Now apply the transfer function
#pragma omp parallel for
            for (unsigned int h=0; h<this->nhex; ++h) {
                this->a[i][h] = this->transfer_a (this->a[i][h], i);
            }
#endif
        }
    }

}; // RD_James
