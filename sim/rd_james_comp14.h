/*
 * 2D Karbowski system with *divisive* normalization of a_i and competition.
 */

#include "rd_james_comp8.h"

template <class Flt>
class RD_James_comp14 : public RD_James_comp8<Flt>
{
public:

    //! Inter-TC-type competition
    //@{
    //! The power to which a_j is raised for the inter-TC axon competition term.
    alignas(Flt) Flt l = 3.0;
    //! epsilon_i parameters. axon competition parameter
    alignas(alignof(vector<Flt>))
    vector<Flt> epsilon;
    //@}

    //! comp3 params
    //@{
    //! The strength of gradient of n(x,t) contribution
    alignas(Flt) Flt E = 0.0;
    //! This holds the two components of the gradient field of the scalar value n(x,t)
    alignas(alignof(array<vector<Flt>, 2>))
    array<vector<Flt>, 2> grad_n;
    //! divergence of n.
    alignas(alignof(vector<Flt>))
    vector<Flt> div_n;
    //@}

    //! comp7 params
    //@{
    //! \hat{a}_i.
    alignas(alignof(vector<Flt>)) vector<Flt> ahat;
    //! \lambda(\hat{a}_i)
    alignas(alignof(vector<Flt>)) vector<Flt> lambda;
    //! gradient \lambda(\hat{a}_i)
    alignas(alignof(array<vector<Flt>, 2>)) array<vector<Flt>, 2> grad_lambda;
    //! Sigmoid offset
    alignas(Flt) Flt o = 5.0;
    //! Sigmoid sharpness
    alignas(Flt) Flt s = 0.5;
    //@}


    RD_James_comp14 (void)
        : RD_James_comp8<Flt>() {
    }

    virtual void allocate (void) {
        RD_James_comp8<Flt>::allocate();

        // epsilon based competition
        this->resize_vector_param (this->epsilon, this->N);

        // comp3
        this->resize_gradient_field (this->grad_n);
        this->resize_vector_variable (this->div_n);

        // comp7
        this->resize_vector_variable (this->ahat);
        this->resize_vector_variable (this->lambda);
        this->resize_gradient_field (this->grad_lambda);
    }

    virtual void init (void) {
        RD_James_comp8<Flt>::init();

        this->zero_gradient_field (this->grad_n);
        this->zero_vector_variable (this->div_n);

        this->zero_vector_variable (this->ahat);
        this->zero_vector_variable (this->lambda);
        this->zero_gradient_field (this->grad_lambda);
    }

    //! Compute divergence of n
    void compute_divn (void) {
#pragma omp parallel for
        for (unsigned int hi=0; hi<this->nhex; ++hi) {
            Flt thesum = -6 * this->n[hi];
            thesum += this->n[(HAS_NE(hi)  ? NE(hi)  : hi)];
            thesum += this->n[(HAS_NNE(hi) ? NNE(hi) : hi)];
            thesum += this->n[(HAS_NNW(hi) ? NNW(hi) : hi)];
            thesum += this->n[(HAS_NW(hi)  ? NW(hi)  : hi)];
            thesum += this->n[(HAS_NSW(hi) ? NSW(hi) : hi)];
            thesum += this->n[(HAS_NSE(hi) ? NSE(hi) : hi)];
            this->div_n[hi] = this->twoover3dd * thesum;
        }
    }

    //! Compute the divergence of J
    void compute_divJ (vector<Flt>& fa, unsigned int i) {

        // Compute gradient of a_i(x), for use computing the third term, below.
        this->spacegrad2D (fa, this->grad_a[i]);

#pragma omp parallel for
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

            // Term 1.1 is E a div(n)
            Flt term1_1 = this->E * fa[hi] * this->div_n[hi];
            if (isnan(term1_1)) {
                cerr << "term1_1 isnan" << endl;
                exit (21);
            }

            // Term 1.2 is E grad(n) . grad(a)
            Flt term1_2 = this->E * (this->grad_n[0][hi] * this->grad_a[i][0][hi]
                                     + this->grad_n[1][hi] * this->grad_a[i][1][hi]);
            if (isnan(term1_2)) {
                cerr << "term1_2 isnan" << endl;
                exit (21);
            }

            // 2. The (a div(g)) term.
            Flt term2 = fa[hi] * this->divg_over3d[i][hi];

            // 3. Third term is this->g . grad a_i. Should not contribute to J, as g(x) decays towards boundary.
            Flt term3 = this->g[i][0][hi] * this->grad_a[i][0][hi] + (this->g[i][1][hi] * this->grad_a[i][1][hi]);

            this->divJ[i][hi] = term1 - term1_1 - term1_2  - term2 - term3;
        }
    }

    virtual void integrate_a (void) {

        // 2. Do integration of a (RK in the 1D model). Involves computing axon branching flux.

        // Pre-compute:
        // 1) The intermediate val alpha_c.
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

            // Compute epsilon * a_hat^l. a_hat is "the sum of all a_j
            // for which j!=i". Call the variable just 'eps'.
            vector<Flt> eps(this->nhex, 0.0);
            for (unsigned int j=0; j<this->N; ++j) {
#define J_NE_I_IS_CRITICAL 1
#ifdef J_NE_I_IS_CRITICAL
                if (j==i) { continue; }
#endif
#pragma omp parallel for
                for (unsigned int h=0; h<this->nhex; ++h) {
                    eps[h] += static_cast<Flt>(pow (this->a[j][h], this->l));
                }
            }

            // Multiply it by epsilon[i]/(N-1). Now it's ready to subtract from the solutions
            Flt eps_over_N = this->epsilon[i]/(this->N-1);
#pragma omp parallel for
            for (unsigned int h=0; h<this->nhex; ++h) {
                eps[h] *= eps_over_N;
            }

            // Runge-Kutta integration for A
            vector<Flt> qq(this->nhex, 0.0);
            this->compute_divJ (this->a[i], i); // populates divJ[i]

            vector<Flt> k1(this->nhex, 0.0);
#pragma omp parallel for
            for (unsigned int h=0; h<this->nhex; ++h) {
                k1[h] = this->divJ[i][h] - this->dc[i][h] - this->a[i][h] * eps[h];
                qq[h] = this->a[i][h] + k1[h] * this->halfdt;
            }
#if 0
            // Code to look at relative contributions of divJ, dc/dt and a*epsilon (competition)
            if ((this->stepCount % 1000) == 0) {
                unsigned int ki = 0;
                cout << "divJ[i][h]=" << this->divJ[i][ki] << " -dc[i][h]=" << -this->dc[i][ki] << " -a*eps=" << -this->a[i][ki] * eps[ki] << endl;
            }
#endif
            vector<Flt> k2(this->nhex, 0.0);
            this->compute_divJ (qq, i);
#pragma omp parallel for
            for (unsigned int h=0; h<this->nhex; ++h) {
                k2[h] = this->divJ[i][h] - this->dc[i][h] - qq[h] * eps[h];
                qq[h] = this->a[i][h] + k2[h] * this->halfdt;
            }

            vector<Flt> k3(this->nhex, 0.0);
            this->compute_divJ (qq, i);
#pragma omp parallel for
            for (unsigned int h=0; h<this->nhex; ++h) {
                k3[h] = this->divJ[i][h] - this->dc[i][h] - qq[h] * eps[h];
                qq[h] = this->a[i][h] + k3[h] * this->dt;
            }

            vector<Flt> k4(this->nhex, 0.0);
            this->compute_divJ (qq, i);

#pragma omp parallel for
            for (unsigned int h=0; h<this->nhex; ++h) {
                k4[h] = this->divJ[i][h] - this->dc[i][h] - qq[h] * eps[h];
                this->a[i][h] += (k1[h] + 2.0 * (k2[h] + k3[h]) + k4[h]) * this->sixthdt;
            }

#if 0
            // Shows that the various ks are all about the same size
            if ((this->stepCount % 1000) == 0) {
                unsigned int ki = 400;
                cout << "k1[ki]:" << k1[ki] << " k2[ki]:" << k2[ki] << " k3[ki]:" << k3[ki] << " k4[ki]:" << k4[ki] << endl;
            }
#endif

            // Do any necessary computation which involves summing a here
            this->sum_a_computation (i);

            // Now apply the transfer function
//#pragma omp parallel for
            for (unsigned int h=0; h<this->nhex; ++h) {
                this->a[i][h] = this->transfer_a (this->a[i][h], i);
            }
        }
    }

    //! Override step() as have to compute div_n and grad_n
    virtual void step (void) {

        this->stepCount++;

        // 1. Compute Karb2004 Eq 3. (coupling between connections made by each TC type)
        this->compute_n();

        // 1.1 Compute divergence and gradient of n
        this->compute_divn();
        this->spacegrad2D (this->n, this->grad_n);

        // 2. Call Runge Kutta numerical integration code
        this->integrate_a();
        this->integrate_c();
    }

}; // RD_James_norm
