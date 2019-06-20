/*
 * 2D Karbowski system with normalization of a_i - intended to be a
 * base class on which to build various types of normalization.
 */

#include "rd_james.h"

template <class Flt>
class RD_James_norm : public RD_James<Flt>
{
public:

    /*!
     * To record dci/dt, as this is used in the computation of a.
     */
    alignas(alignof(vector<vector<Flt> >))
    vector<vector<Flt> > dc;

    /*!
     * Simple constructor; no arguments. Just calls base constructor.
     */
    RD_James_norm (void)
        : RD_James<Flt>() {
    }

    /*!
     * Override allocate() and init(), and add a couple of extra
     * resizes.
     */
    //@{
    virtual void allocate (void) {
        RD_James<Flt>::allocate();
        this->resize_vector_vector (this->dc, this->N);

    }
    virtual void init (void) {
        cout << "RD_James_norm::init() called" << endl;
        RD_James<Flt>::init();
    }
    //@}

    /*!
     * Computation methods
     */
    //@{

    virtual void integrate_c (void) {
        // 3. Do integration of c
        for (unsigned int i=0; i<this->N; ++i) {

#pragma omp parallel for
            for (unsigned int h=0; h<this->nhex; h++) {
                // Note: betaterm used in compute_dci_dt()
                this->betaterm[i][h] = this->beta[i] * this->n[h] * static_cast<Flt>(pow (this->a[i][h], this->k));
            }

            // Runge-Kutta integration for C (or ci)
            vector<Flt> qq(this->nhex,0.);
            vector<Flt> k1 = this->compute_dci_dt (this->c[i], i);
#pragma omp parallel for
            for (unsigned int h=0; h<this->nhex; h++) {
                qq[h] = this->c[i][h] + k1[h] * this->halfdt;
            }

            vector<Flt> k2 = this->compute_dci_dt (qq, i);
#pragma omp parallel for
            for (unsigned int h=0; h<this->nhex; h++) {
                qq[h] = this->c[i][h] + k2[h] * this->halfdt;
            }

            vector<Flt> k3 = this->compute_dci_dt (qq, i);
#pragma omp parallel for
            for (unsigned int h=0; h<this->nhex; h++) {
                qq[h] = this->c[i][h] + k3[h] * this->dt;
            }

            vector<Flt> k4 = this->compute_dci_dt (qq, i);
#pragma omp parallel for
            for (unsigned int h=0; h<this->nhex; h++) {
                this->dc[i][h] = (k1[h]+2. * (k2[h] + k3[h]) + k4[h]) * this->sixthdt;
                Flt c_cand = this->c[i][h] + this->dc[i][h];
                // Avoid over-saturating c_i and make sure dc is similarly modified.
                this->dc[i][h] = (c_cand > 1.0) ? (1.0 - this->c[i][h]) : this->dc[i][h];
                this->c[i][h] = (c_cand > 1.0) ? 1.0 : c_cand;
            }
        }
    }

    /*!
     * A possibly normalization-function specific task to carry out
     * once after the sum of a has been computed.
     */
    virtual void sum_a_computation (const unsigned int _i) {}

    /*!
     * The normalization/transfer function.
     */
    virtual inline Flt transfer_a (const Flt& _a, const unsigned int _i) {
        Flt a_rtn = _a;
        return a_rtn;
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

            // Runge-Kutta integration for A
            vector<Flt> qq(this->nhex, 0.0);
            this->compute_divJ (this->a[i], i); // populates divJ[i]

            vector<Flt> k1(this->nhex, 0.0);
#pragma omp parallel for
            for (unsigned int h=0; h<this->nhex; ++h) {
                k1[h] = this->divJ[i][h] - this->dc[i][h];
                qq[h] = this->a[i][h] + k1[h] * this->halfdt;
            }

            vector<Flt> k2(this->nhex, 0.0);
            this->compute_divJ (qq, i);
#pragma omp parallel for
            for (unsigned int h=0; h<this->nhex; ++h) {
                k2[h] = this->divJ[i][h] - this->dc[i][h];
                qq[h] = this->a[i][h] + k2[h] * this->halfdt;
            }

            vector<Flt> k3(this->nhex, 0.0);
            this->compute_divJ (qq, i);
#pragma omp parallel for
            for (unsigned int h=0; h<this->nhex; ++h) {
                k3[h] = this->divJ[i][h] - this->dc[i][h];
                qq[h] = this->a[i][h] + k3[h] * this->dt;
            }

            vector<Flt> k4(this->nhex, 0.0);
            this->compute_divJ (qq, i);
#pragma omp parallel for
            for (unsigned int h=0; h<this->nhex; ++h) {
                k4[h] = this->divJ[i][h] - this->dc[i][h];
                this->a[i][h] += (k1[h] + 2.0 * (k2[h] + k3[h]) + k4[h]) * this->sixthdt;
            }

            // Do any necessary computation which involves summing a here
            this->sum_a_computation (i);

            // Now apply the transfer function
//#define DEBUG_SUM_A_TRANSFERRED 1
#ifdef DEBUG_SUM_A_TRANSFERRED
            Flt sum_a_transferred = 0.0;
#endif
#ifndef DEBUG_SUM_A_TRANSFERRED
# pragma omp parallel for
#endif
            for (unsigned int h=0; h<this->nhex; ++h) {
                this->a[i][h] = this->transfer_a (this->a[i][h], i);
#ifdef DEBUG_SUM_A_TRANSFERRED
                sum_a_transferred += this->a[i][h];
#endif
            }
#ifdef DEBUG_SUM_A_TRANSFERRED
            cout << "After transfer_a(), sum_a is " << sum_a_transferred << endl;
#endif
        }
    }

    /*!
     * Compute n
     */
    virtual void compute_n (void) {

        Flt nsum = 0.0;
        Flt csum = 0.0;
#pragma omp parallel for reduction(+:nsum,csum)
        for (unsigned int hi=0; hi<this->nhex; ++hi) {
            this->n[hi] = 0;
            // First, use n[hi] so sum c over all i:
            for (unsigned int i=0; i<this->N; ++i) {
                this->n[hi] += this->c[i][hi];
            }
            // Prevent sum of c being too large:
            this->n[hi] = (this->n[hi] > 1.0) ? 1.0 : this->n[hi];
            csum += this->c[0][hi];
            // Now compute n for real:
            this->n[hi] = 1. - this->n[hi];
            nsum += this->n[hi];
        }

#ifdef DEBUG__
        if (this->stepCount % 100 == 0) {
            DBG ("System computed " << this->stepCount << " times so far...");
            DBG ("sum of n+c is " << nsum+csum);
        }
#endif
    }

    /*!
     * Do a single step through the model.
     */
    virtual void step (void) {

        this->stepCount++;

        // 1. Compute Karb2004 Eq 3. (coupling between connections made by each TC type)
        this->compute_n();

        // 2. Call Runge Kutta numerical integration code
        this->integrate_a();
        this->integrate_c();
    }

}; // RD_James_norm
