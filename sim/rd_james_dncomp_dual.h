/*
 * 2D Karbowski system with *divisive* normalization of a_i AND competition AND the ability to run
 * two simulations coupled by divisive normalisation across the two regions.
 */

#include "rd_james_dncomp.h"

template <class Flt>
class RD_James_dncomp_dual : public RD_James_dncomp<Flt>
{
public:

    /*!
     * Hold a pointer to the "mirror" simulation
     */
    alignas (alignof(RD_James_dncomp_dual*)) RD_James_dncomp_dual* mirror;

    RD_James_dncomp_dual (void)
        : RD_James_dncomp<Flt>() {
    }

    virtual void allocate (void) {
        RD_James_dncomp<Flt>::allocate();
        // Anything additional
    }

    //! A function to call after both self and the mirror have been initilalised, called only from
    //! the 'self' object.
    void init_sums (void) {
        for (unsigned int i=0; i<this->N; ++i) {
            this->sum_a[i] += this->mirror->sum_a[i];
            this->mirror->sum_a[i] = this->sum_a[i];
        }
    }

    //! Do summation using both self and mirror
    virtual void summation_a (void) {
        for (unsigned int i=0; i<this->N; ++i) {
            // Do any necessary computation which involves summing a here
            this->sum_a_computation (i); // sum_a contains N sums
            this->mirror->sum_a_computation (i); //mirror->sum_a contains N sums

            // Now add sum_a and mirror->sum_a so that transfer function takes into account the sum
            // across self and mirror:
            this->sum_a[i] += this->mirror->sum_a[i];
            this->mirror->sum_a[i] = this->sum_a[i];
        }
    }

    //! Apply transfer function to all N TC types to complete the normalization
    void transference_a (void) {
        for (unsigned int i=0; i<this->N; ++i) {
#pragma omp parallel for
            for (unsigned int h=0; h<this->nhex; ++h) {
                this->a[i][h] = this->transfer_a (this->a[i][h], i);
            }
        }
    }

    void step0 (void) {
#ifdef PROFILE_CODE
        if ((this->stepCount % 100) == 0) {
            if (!this->codetimes.empty()) {
                this->codetimes.back().output();
            }
            Codetime ct;
            this->codetimes.push_back (ct);
        }
#endif
        this->stepCount++;
        // 1. Compute Karb2004 Eq 3. (coupling between connections made by each TC type)
        this->compute_n();
        // 1.1 Compute divergence and gradient of n
        this->compute_divn();
        this->spacegrad2D (this->n, this->grad_n);
        // 2. Call Runge Kutta numerical integration code on a
        this->integrate_a();
    }

    //! Override step() as we have to coordinate computations in the two objects; self and mirror.
    virtual void step (void) {

        // Do the first, independent steps on self, then on mirror:
        this->step0();
        this->mirror->step0();

        // Do summation here. THIS version of summation_a() sums based both on self and mirror, and
        // updates the sums in both self and mirror.
        this->summation_a();
        // Apply the transfer function to self and mirror:
        this->transference_a();
        this->mirror->transference_a();

        // Do the final independent steps on self, then on mirror:
        this->integrate_c();
        this->mirror->integrate_c();
    }

}; // RD_James_dncomp_dual
