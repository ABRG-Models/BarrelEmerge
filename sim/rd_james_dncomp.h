/*
 * 2D Karbowski system with *divisive* normalization of a_i AND competition.
 */

#include "rd_james_divnorm.h"

#include <chrono>
using namespace std::chrono;

// Counting up the time taken on each section.
class Codetime
{
public:
    milliseconds compute_n_time = std::chrono::milliseconds::zero();
    milliseconds compute_divn_time = std::chrono::milliseconds::zero();
    milliseconds compute_spacegrad_n_time = std::chrono::milliseconds::zero();
    milliseconds integrate_a_time = std::chrono::milliseconds::zero();
    milliseconds integrate_c_time = std::chrono::milliseconds::zero();

    milliseconds a_precompute = std::chrono::milliseconds::zero();
    milliseconds a_eps_all = std::chrono::milliseconds::zero();
    milliseconds a_for1 = std::chrono::milliseconds::zero();
    milliseconds a_for2 = std::chrono::milliseconds::zero();
    milliseconds a_for3 = std::chrono::milliseconds::zero();
    milliseconds a_for4 = std::chrono::milliseconds::zero();
    milliseconds a_for5 = std::chrono::milliseconds::zero();
    milliseconds a_for6 = std::chrono::milliseconds::zero();

    void output (void) const {
        cout << "Compute... n: " << compute_n_time.count()
             << ", divn: " << compute_divn_time.count()
             << ", gradn: " << compute_spacegrad_n_time.count()
             << ", a: " << integrate_a_time.count()
             << ", c: " << integrate_c_time.count()
             << endl;
        cout << "Compute... a_pre: " << a_precompute.count()
             << ", a_eps_all: " << a_eps_all.count()
             << ", for1, : " << a_for1.count()
             << ", for2, : " << a_for2.count()
             << ", for3, : " << a_for3.count()
             << ", for4, : " << a_for4.count()
             << ", for5, : " << a_for5.count()
             << ", for6, : " << a_for6.count()
             << endl;
    }
};

template <class Flt>
class RD_James_dncomp : public RD_James_divnorm<Flt>
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


    RD_James_dncomp (void)
        : RD_James_divnorm<Flt>() {
    }

    virtual void allocate (void) {
        RD_James_divnorm<Flt>::allocate();

        // epsilon based competition
        this->resize_vector_param (this->epsilon, this->N);

        // comp3
        this->resize_gradient_field (this->grad_n);
        this->resize_vector_variable (this->div_n);

        // comp7
        this->resize_vector_variable (this->ahat);
        this->resize_vector_variable (this->lambda);
        this->resize_gradient_field (this->grad_lambda);

        // eps
        this->resize_vector_variable (this->eps_all);
        this->resize_vector_variable (this->eps_i);
        this->resize_vector_variable (this->eps);
    }

    virtual void init (void) {
        RD_James_divnorm<Flt>::init();

        this->zero_gradient_field (this->grad_n);
        this->zero_vector_variable (this->div_n);

        this->zero_vector_variable (this->ahat);
        this->zero_vector_variable (this->lambda);
        this->zero_gradient_field (this->grad_lambda);
    }

    //! Compute divergence of n
    void compute_divn (void) {
//#pragma omp parallel for
        for (unsigned int hi=0; hi<this->nhex; ++hi) {
            Flt thesum = -6 * this->n[hi];
            thesum += this->n[(HAS_NE(hi)  ? NE(hi)  : hi)];
            if (isnan(thesum)) {
                cerr << "at hi=" << hi << ", n[" << (HAS_NE(hi)  ? NE(hi)  : hi) << "] isnan" << endl;
            }
            thesum += this->n[(HAS_NNE(hi) ? NNE(hi) : hi)];
            if (isnan(thesum)) {
                cerr << "at hi=" << hi << ", n[" << (HAS_NNE(hi)  ? NNE(hi)  : hi) << "] isnan" << endl;
            }
            thesum += this->n[(HAS_NNW(hi) ? NNW(hi) : hi)];
            if (isnan(thesum)) {
                cerr << "at hi=" << hi << ", n[" << (HAS_NNW(hi)  ? NNW(hi)  : hi) << "] isnan" << endl;
            }
            thesum += this->n[(HAS_NW(hi)  ? NW(hi)  : hi)];
            if (isnan(thesum)) {
                cerr << "at hi=" << hi << ", n[" << (HAS_NW(hi)  ? NW(hi)  : hi) << "] isnan" << endl;
            }
            thesum += this->n[(HAS_NSW(hi) ? NSW(hi) : hi)];
            if (isnan(thesum)) {
                cerr << "at hi=" << hi << ", n[" << (HAS_NSW(hi)  ? NSW(hi)  : hi) << "] isnan" << endl;
            }
            thesum += this->n[(HAS_NSE(hi) ? NSE(hi) : hi)];
            if (isnan(thesum)) {
                cerr << "at hi=" << hi << ", n[" << (HAS_NSE(hi)  ? NSE(hi)  : hi) << "] isnan" << endl;
                cerr << "(at end) thesum isnan in compute_divn" << endl;
            }
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
                if (isnan(this->E)) {
                    cerr << "E isnan" << endl;
                }
                if (isnan(fa[hi])) {
                    cerr << "fa[hi] isnan" << endl;
                }
                if (isnan(div_n[hi])) {
                    cerr << "div_n[hi="<<hi<<"] isnan" << endl;
                }
                exit (21);
            }

            // Term 1.2 is E grad(n) . grad(a)
            Flt term1_2 = this->E * (this->grad_n[0][hi] * this->grad_a[i][0][hi]
                                     + this->grad_n[1][hi] * this->grad_a[i][1][hi]);
            if (isnan(term1_2)) {
                cerr << "term1_2 isnan" << endl;
                if (isnan(this->E)) {
                    cerr << "E isnan" << endl;
                }
                if (isnan(this->grad_n[0][hi])) {
                    cerr << "this->grad_n[0][hi] isnan" << endl;
                }
                if (isnan(this->grad_a[i][0][hi])) {
                    cerr << "this->grad_a[i][0][hi] isnan" << endl;
                }
                if (isnan(this->grad_a[i][1][hi])) {
                    cerr << "this->grad_a[i][1][hi] isnan" << endl;
                }
                exit (21);
            }
#if 0
            // 2. The (a div(g)) term.
            Flt term2 = fa[hi] * this->divg_over3d[i][hi];

            // 3. Third term is this->g . grad a_i. Should not contribute to J, as g(x) decays towards boundary.
            Flt term3 = this->g[i][0][hi] * this->grad_a[i][0][hi] + (this->g[i][1][hi] * this->grad_a[i][1][hi]);
#endif
            // 2. The (a div(g)) term.
            Flt term2 = 0.0;

            // 3. Third term is this->g . grad a_i. Should not contribute to J, as g(x) decays towards boundary.
            Flt term3 = 0.0;

            for (unsigned int m =0 ; m < this->M; ++m) {
                if (this->stepCount >= this->guidance_time_onset[m]) {
                    // g contributes to term2
                    term2 += fa[hi] * this->divg_over3d[m][i][hi];
                    // and to term3
                    term3 += this->g[m][i][0][hi] * this->grad_a[i][0][hi] + (this->g[m][i][1][hi] * this->grad_a[i][1][hi]);
                }
            }

            this->divJ[i][hi] = term1 - term1_1 - term1_2  - term2 - term3;
            if (isnan(this->divJ[i][hi])) {
                cerr << "divJ[i="<<i<<"][hi="<<hi<<"] isnan" << endl;
            }
        }
    }

    //! Used as a temporary variable.
    vector<Flt> eps_all; // sum of all a^l
    vector<Flt> eps_i; // sum of a^l for TC index i
    vector<Flt> eps; // eps_all - eps_i

    virtual void integrate_a (void) {

        milliseconds ms1 = duration_cast<milliseconds>(system_clock::now().time_since_epoch());
        // 2. Do integration of a (RK in the 1D model). Involves computing axon branching flux.

        // Pre-compute:
        // 1) The intermediate val alpha_c.
        for (unsigned int i=0; i<this->N; ++i) {
#pragma omp parallel for
            for (unsigned int h=0; h<this->nhex; ++h) {
                this->alpha_c[i][h] = this->alpha[i] * this->c[i][h];
            }
        }
        milliseconds ms2 = duration_cast<milliseconds>(system_clock::now().time_since_epoch());
        this->codetimes.back().a_precompute += (ms2-ms1);

        // Compute eps_all once only
        this->zero_vector_variable (this->eps_all);
        for (unsigned int j=0; j<this->N; ++j) {
#pragma omp parallel for
            for (unsigned int h=0; h<this->nhex; ++h) {
                eps_all[h] += static_cast<Flt>(pow (this->a[j][h], this->l));
            }
        }

        milliseconds ms3 = duration_cast<milliseconds>(system_clock::now().time_since_epoch());
        this->codetimes.back().a_eps_all += (ms3-ms2);

        // Runge-Kutta:
        // No OMP here - there are only N(<10) loops, which isn't
        // enough to load the threads up.
        for (unsigned int i=0; i<this->N; ++i) {

            milliseconds msf1 = duration_cast<milliseconds>(system_clock::now().time_since_epoch());

            //this->zero_vector_variable (this->eps_i);

            // Compute epsilon * a_hat^l. a_hat is "the sum of all a_j
            // for which j!=i". Call the variable just 'eps'.

            // Compute eps_i, for subtraction from eps_all
#pragma omp parallel for // slows down with or without parallel for
            for (unsigned int h=0; h<this->nhex; ++h) {
                eps_i[h] = static_cast<Flt>(pow (this->a[i][h], this->l));
            }

            milliseconds msf2 = duration_cast<milliseconds>(system_clock::now().time_since_epoch());
            this->codetimes.back().a_for1 += (msf2-msf1);

            // Multiply it by epsilon[i]/(N-1). Now it's ready to subtract from the solutions
            Flt eps_over_N = this->epsilon[i]/(this->N-1);
#pragma omp parallel for
            for (unsigned int h=0; h<this->nhex; ++h) {
                eps[h] = (eps_all[h]-eps_i[h]) * eps_over_N;
            }

            milliseconds msf3 = duration_cast<milliseconds>(system_clock::now().time_since_epoch());
            this->codetimes.back().a_for2 += (msf3-msf2);

            // Runge-Kutta integration for A
            vector<Flt> qq(this->nhex, 0.0);
            this->compute_divJ (this->a[i], i); // populates divJ[i]

            milliseconds msf4 = duration_cast<milliseconds>(system_clock::now().time_since_epoch());
            this->codetimes.back().a_for3 += (msf4-msf3);

            vector<Flt> k1(this->nhex, 0.0);
#pragma omp parallel for
            for (unsigned int h=0; h<this->nhex; ++h) {
                k1[h] = this->divJ[i][h] - this->dc[i][h] - this->a[i][h] * eps[h];
                qq[h] = this->a[i][h] + k1[h] * this->halfdt;
            }

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

#pragma omp__ parallel for
            for (unsigned int h=0; h<this->nhex; ++h) {
                k4[h] = this->divJ[i][h] - this->dc[i][h] - qq[h] * eps[h];
                if (isinf(eps[h])) { cerr << "eps[h="<<h<<"] isinf" << endl; }
                if (isnan(eps[h])) { cerr << "eps[h="<<h<<"] isnan" << endl; }
                if (isinf(qq[h])) { cerr << "qq[h="<<h<<"] isinf" << endl; }
                if (isnan(qq[h])) { cerr << "qq[h="<<h<<"] isnan" << endl; }
                if (isinf(this->dc[i][h])) { cerr << "dc[i][h="<<h<<"] isinf" << endl; }
                if (isnan(this->dc[i][h])) { cerr << "dc[i][h="<<h<<"] isnan" << endl; }
                if (isinf(this->divJ[i][h])) { cerr << "divJ[i][h="<<h<<"] isinf" << endl; }
                if (isnan(this->divJ[i][h])) { cerr << "divJ[i][h="<<h<<"] isnan" << endl; }
                if (isinf(k4[h])) {
                    cerr << "k4[h="<<h<<"] isinf" << endl;

                    cerr << "k4[h] = " << this->divJ[i][h] << " - " <<  this->dc[i][h] << " - " << qq[h] << " * " << eps[h] << endl;

                }
                if (isnan(k4[h])) { cerr << "k4[h="<<h<<"] isnan" << endl; }
                this->a[i][h] += (k1[h] + 2.0 * (k2[h] + k3[h]) + k4[h]) * this->sixthdt;
            }

            milliseconds msf5 = duration_cast<milliseconds>(system_clock::now().time_since_epoch());
            this->codetimes.back().a_for4 += (msf5-msf4);

            // Do any necessary computation which involves summing a here
            this->sum_a_computation (i);

            milliseconds msf6 = duration_cast<milliseconds>(system_clock::now().time_since_epoch());
            this->codetimes.back().a_for5 += (msf6-msf5);

            // Now apply the transfer function
#pragma omp__ parallel for
            for (unsigned int h=0; h<this->nhex; ++h) {
                if (isinf(this->a[i][h])) {
                    cerr << "Before transfer_a, a[i="<<i<<"][h="<<h<<"] isinf" << endl;
                }
                Flt ta = this->transfer_a (this->a[i][h], i);
                if (isnan(ta)) {
                    cerr << "Before transfer_a, a[i="<<i<<"][h="<<h<<"] = " << this->a[i][h] << endl;
                    cerr << "AFTER transfer_a, a[i="<<i<<"][h="<<h<<"] is(gonnabe)nan" << endl;
                }
                this->a[i][h] = ta;
            }

            milliseconds msf7 = duration_cast<milliseconds>(system_clock::now().time_since_epoch());
            this->codetimes.back().a_for6 += (msf7-msf6);
        }
    }

    //! Counters for timing.
    vector<Codetime> codetimes;

    //! Override step() as have to compute div_n and grad_n
    virtual void step (void) {

        if ((this->stepCount % 100) == 0) {
            if (!codetimes.empty()) {
                codetimes.back().output();
            }
            Codetime ct;
            codetimes.push_back (ct);
        }
        this->stepCount++;

        milliseconds ms1 = duration_cast<milliseconds>(system_clock::now().time_since_epoch());
        // 1. Compute Karb2004 Eq 3. (coupling between connections made by each TC type)
        this->compute_n();

        milliseconds ms2 = duration_cast<milliseconds>(system_clock::now().time_since_epoch());
        codetimes.back().compute_n_time += (ms2-ms1);
        // 1.1 Compute divergence and gradient of n
        this->compute_divn();
        milliseconds ms3 = duration_cast<milliseconds>(system_clock::now().time_since_epoch());
        codetimes.back().compute_divn_time += (ms3-ms2);
        this->spacegrad2D (this->n, this->grad_n);
        milliseconds ms4 = duration_cast<milliseconds>(system_clock::now().time_since_epoch());
        codetimes.back().compute_spacegrad_n_time += (ms4-ms3);

        // 2. Call Runge Kutta numerical integration code
        this->integrate_a();
        milliseconds ms5 = duration_cast<milliseconds>(system_clock::now().time_since_epoch());
        codetimes.back().integrate_a_time += (ms5-ms4);
        this->integrate_c();
        milliseconds ms6 = duration_cast<milliseconds>(system_clock::now().time_since_epoch());
        codetimes.back().integrate_c_time += (ms6-ms5);
    }

}; // RD_James_norm
