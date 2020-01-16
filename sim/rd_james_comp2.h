/*
 * Competition method 2, which implements Eq. 34 in the lab notes
 * (rd_karbowski.pdf; label eq:Karb2D_J_NM_with_comp2_impl)
 */

#include "rd_james.h"

template <class Flt>
class RD_James_comp2 : public RD_James<Flt>
{
public:
    /*!
     * Parameter which controls the strength of diffusion away from
     * axon branching of other TC types.
     */
    alignas(Flt) Flt F = 0.2;
    alignas(Flt) Flt FOverNm1 = 0.0;

    /*!
     * \hat{a}_i. Recomputed for each new i, so doesn't need to be a
     * vector of vectors.
     */
    alignas(alignof(vector<Flt>))
    vector<Flt> ahat;

    /*!
     * This holds the two components of the gradient field of the
     * scalar value \hat{a}_i(x,t), which is the sum of the branching
     * densities of all axon types except i.
     */
    alignas(alignof(array<vector<Flt>, 2>))
    array<vector<Flt>, 2> grad_ahat;

    /*!
     * divergence of \hat{a}_i(x,t).
     */
    alignas(alignof(vector<Flt>))
    vector<Flt> div_ahat;

    /*!
     * \bar{a}_i - result of processing a_i through a sigmoid.
     */
    //@{
    alignas(alignof(vector<Flt>))
    vector<Flt> abar;
    alignas(alignof(array<vector<Flt>, 2>))
    array<vector<Flt>, 2> grad_abar;
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
    }
    virtual void init (void) {
        RD_James<Flt>::init();
        this->zero_vector_variable (this->ahat);
        this->zero_gradient_field (this->grad_ahat);
        this->zero_vector_variable (this->div_ahat);
        this->zero_vector_variable (this->abar);
        this->zero_gradient_field (this->grad_abar);
    }
    //@}
    /*!
     * Computation methods
     */
    //@{

    /*!
     * Do a single step through the model.
     */
    void step (void) {

        this->stepCount++;

        // 1. Compute Karb2004 Eq 3. (coupling between connections made by each TC type)
        Flt nsum = 0.0;
        Flt csum = 0.0;
#pragma omp parallel for reduction(+:nsum,csum)
        for (unsigned int hi=0; hi<this->nhex; ++hi) {
            this->n[hi] = 0;
            for (unsigned int i=0; i<this->N; ++i) {
                this->n[hi] += this->c[i][hi];
            }
            // Prevent sum of c being too large:
            this->n[hi] = (this->n[hi] > 1.0) ? 1.0 : this->n[hi];
            csum += this->c[0][hi];
            this->n[hi] = 1. - this->n[hi];
            nsum += this->n[hi];
        }

#ifdef DEBUG__
        if (this->stepCount % 100 == 0) {
            DBG ("System computed " << this->stepCount << " times so far...");
            DBG ("sum of n+c is " << nsum+csum);
        }
#endif

        // 2. Do integration of a (RK in the 1D model). Involves computing axon branching flux.

        // Pre-compute intermediate val:
        for (unsigned int i=0; i<this->N; ++i) {
#pragma omp parallel for
            for (unsigned int h=0; h<this->nhex; ++h) {
                this->alpha_c[i][h] = this->alpha[i] * this->c[i][h];
            }
        }

        // Runge-Kutta:
        // No OMP here - there are only N(<10) loops, which isn't
        // enough to load the threads up.
        for (unsigned int i=0; i<this->N; ++i) {

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

            // Runge-Kutta integration for A
            vector<Flt> q(this->nhex, 0.0);
            this->compute_divJ (this->a[i], i); // populates divJ[i]

            vector<Flt> k1(this->nhex, 0.0);
#pragma omp parallel for
            for (unsigned int h=0; h<this->nhex; ++h) {
                k1[h] = this->divJ[i][h] + this->alpha_c[i][h] - this->beta[i] * this->n[h] * static_cast<Flt>(pow (this->a[i][h], this->k));
                q[h] = this->a[i][h] + k1[h] * this->halfdt;
            }

            vector<Flt> k2(this->nhex, 0.0);
            this->compute_divJ (q, i);
#pragma omp parallel for
            for (unsigned int h=0; h<this->nhex; ++h) {
                k2[h] = this->divJ[i][h] + this->alpha_c[i][h] - this->beta[i] * this->n[h] * static_cast<Flt>(pow (q[h], this->k));
                q[h] = this->a[i][h] + k2[h] * this->halfdt;
            }

            vector<Flt> k3(this->nhex, 0.0);
            this->compute_divJ (q, i);
#pragma omp parallel for
            for (unsigned int h=0; h<this->nhex; ++h) {
                k3[h] = this->divJ[i][h] + this->alpha_c[i][h] - this->beta[i] * this->n[h] * static_cast<Flt>(pow (q[h], this->k));
                q[h] = this->a[i][h] + k3[h] * this->dt;
            }

            vector<Flt> k4(this->nhex, 0.0);
            this->compute_divJ (q, i);
#pragma omp parallel for
            for (unsigned int h=0; h<this->nhex; ++h) {
                k4[h] = this->divJ[i][h] + this->alpha_c[i][h] - this->beta[i] * this->n[h] * static_cast<Flt>(pow (q[h], this->k));
                this->a[i][h] += (k1[h] + 2.0 * (k2[h] + k3[h]) + k4[h]) * this->sixthdt;
                // Prevent a from becoming negative:
                this->a[i][h] = (this->a[i][h] < 0.0) ? 0.0 : this->a[i][h];
            }
            //cout << "a[" << i << "][0] = " << this->a[i][0] << endl;
            if (isnan(this->a[i][0])) {
                cerr << "Exiting on a[i][0] == NaN" << endl;
                exit (1);
            }
        }

        // 3. Do integration of c
        for (unsigned int i=0; i<this->N; ++i) {

#pragma omp parallel for
            for (unsigned int h=0; h<this->nhex; h++) {
                // Note: betaterm used in compute_dci_dt()
                this->betaterm[i][h] = this->beta[i] * this->n[h] * static_cast<Flt>(pow (this->a[i][h], this->k));
            }

            // Runge-Kutta integration for C (or ci)
            vector<Flt> q(this->nhex,0.);
            vector<Flt> k1 = this->compute_dci_dt (this->c[i], i);
#pragma omp parallel for
            for (unsigned int h=0; h<this->nhex; h++) {
                q[h] = this->c[i][h] + k1[h] * this->halfdt;
            }

            vector<Flt> k2 = this->compute_dci_dt (q, i);
#pragma omp parallel for
            for (unsigned int h=0; h<this->nhex; h++) {
                q[h] = this->c[i][h] + k2[h] * this->halfdt;
            }

            vector<Flt> k3 = this->compute_dci_dt (q, i);
#pragma omp parallel for
            for (unsigned int h=0; h<this->nhex; h++) {
                q[h] = this->c[i][h] + k3[h] * this->dt;
            }

            vector<Flt> k4 = this->compute_dci_dt (q, i);
#pragma omp parallel for
            for (unsigned int h=0; h<this->nhex; h++) {
                this->c[i][h] += (k1[h]+2. * (k2[h] + k3[h]) + k4[h]) * this->sixthdt;
                // Avoid over-saturating c_i:
                this->c[i][h] = (this->c[i][h] > 1.0) ? 1.0 : this->c[i][h];
            }
#if 0
            cout << "c[" << i << "][0] = " << this->c[i][0] << endl;
            if (isnan(this->c[i][0])) {
                cerr << "Exiting on c[i][0] == NaN" << endl;
                exit (2);
            }
#endif
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
                cerr << "div ahat isnan" << endl;
                exit (3);
            }
        }
    }

    /*!
     * Computes the "flux of axonal branches" term, J_i(x) (Eq 4)
     *
     * Inputs: this->g, fa (which is this->a[i] or a q in the RK
     * algorithm), this->D, @a i, the TC type.  Helper functions:
     * spacegrad2D().  Output: this->divJ
     *
     * Stable with dt = 0.0001;
     */
    void compute_divJ (vector<Flt>& fa, unsigned int i) {

        // Compute \bar{a}_i and its spatial gradient
        Flt h = 2.0; // height parameter for sigmoid
        Flt o = 5.0; // offset
        Flt s = 0.5; // sharpness
#pragma omp parallel for
        for (unsigned int hi=0; hi<this->nhex; ++hi) {
            this->abar[hi] = h / (1 - exp (o - s * fa[hi]));
        }
        this->spacegrad2D (this->abar, this->grad_abar);

        // Compute gradient of a_i(x), for use computing the third term, below.
        this->spacegrad2D (fa, this->grad_a[i]);

        if (this->N > 0) {
            this->FOverNm1 = this->F/(this->N-1);
        } else {
            this->FOverNm1 = 0.0;
        }

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
                cerr << "term1 isnan" << endl;
                cerr << "thesum is " << thesum << " fa[hi=" << hi << "] = " << fa[hi] << endl;
                exit (21);
            }

            // Term 1.1 is F/N-1 abar div(ahat)
            Flt term1_1 = this->FOverNm1 * abar[hi] * this->div_ahat[hi];
            if (isnan(term1_1)) {
                cerr << "term1_1 isnan" << endl;
                cerr << "fa[hi="<<hi<<"] = " << fa[hi] << ", this->div_ahat[hi] = " << this->div_ahat[hi] << endl;
                exit (21);
            }

            // Term 1.2 is F/N-1 grad(ahat) . grad(abar)
            Flt term1_2 = this->FOverNm1 * (this->grad_ahat[0][hi] * this->grad_abar[0][hi]
                                            + this->grad_ahat[1][hi] * this->grad_abar[1][hi]);
            if (isnan(term1_2)) {
                cerr << "term1_2 isnan" << endl;
                exit (21);
            }

            // 2. The (a div(g)) term.
            Flt term2 = fa[hi] * this->divg_over3d[i][hi];

            if (isnan(term2)) {
                cerr << "term2 isnan" << endl;
                exit (21);
            }

            // 3. Third term is this->g . grad a_i. Should not contribute to J, as g(x) decays towards boundary.
            Flt term3 = this->g[i][0][hi] * this->grad_a[i][0][hi] + (this->g[i][1][hi] * this->grad_a[i][1][hi]);

            if (isnan(term3)) {
                cerr << "term3 isnan" << endl;
                exit (30);
            }

            this->divJ[i][hi] = term1 - term1_1 - term1_2 - term2 - term3;
        }
    }

}; // RD_James
