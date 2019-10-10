/*
 * 2D Karbowski system with *divisive* normalization of a_i AND competition AND
 * per-group competition.
 */

#include "rd_james_dncomp.h"

template <class Flt>
class RD_James_dncomp2 : public RD_James_dncomp<Flt>
{
public:

    //! Inter-TC-type competition
    //@{
    //! xi_i parameters. axon competition parameter 2
    alignas(alignof(vector<Flt>)) vector<Flt> xi;
    //! Used as a temporary variables
    //@{
    //! sum of a^l for the group to which i belongs
    alignas(alignof(vector<Flt>)) vector<Flt> xi_group_i;
    //! eps_all - xi_group_i
    alignas(alignof(vector<Flt>)) vector<Flt> xi_final;
    //@}
    //@}

    RD_James_dncomp2 (void)
        : RD_James_dncomp<Flt>() {
    }

    virtual void allocate (void) {
        RD_James_dncomp<Flt>::allocate();
        // competition
        this->resize_vector_param (this->xi, this->N);
        // Temp variables
        this->resize_vector_variable (this->xi_group_i);
        this->resize_vector_variable (this->xi_final);
    }

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
                this->eps_all[h] += static_cast<Flt>(pow (this->a[j][h], this->l));
            }
        }

        milliseconds ms3 = duration_cast<milliseconds>(system_clock::now().time_since_epoch());
        this->codetimes.back().a_eps_all += (ms3-ms2);

        // Runge-Kutta:
        // No OMP here - there are only N(<10) loops, which isn't
        // enough to load the threads up.
        for (unsigned int i=0; i<this->N; ++i) {

            milliseconds msf1 = duration_cast<milliseconds>(system_clock::now().time_since_epoch());

            // Compute epsilon * a_hat^l. a_hat is "the sum of all a_j
            // for which j!=i". Call the variable just 'eps'.

            // Compute eps_i, for subtraction from eps_all
#pragma omp parallel for // slows down with or without parallel for
            for (unsigned int h=0; h<this->nhex; ++h) {
                this->eps_i[h] = static_cast<Flt>(pow (this->a[i][h], this->l));
            }

            this->zero_vector_variable (this->xi_group_i);
            // For each j, is j in group i? If so, add to xi_group_i
            for (unsigned int j = 0; j<this->N; ++j) {
                if (this->group[j] == this->group[i]) {
#pragma omp parallel for
                    for (unsigned int h=0; h<this->nhex; ++h) {
                        xi_group_i[h] += static_cast<Flt>(pow (this->a[j][h], this->l));
                    }
                }
            }

            milliseconds msf2 = duration_cast<milliseconds>(system_clock::now().time_since_epoch());
            this->codetimes.back().a_for1 += (msf2-msf1);

            // Multiply it by epsilon[i]/(N-1). Now it's ready to subtract from the solutions
            Flt eps_over_N = this->epsilon[i]/(this->N-1);
            Flt xi_over_N = this->xi[i]/(this->N-this->groupset.size());
#pragma omp parallel for
            for (unsigned int h=0; h<this->nhex; ++h) {
                this->eps[h] = (this->eps_all[h]-this->eps_i[h]) * eps_over_N;
                xi_final[h] = (this->eps_all[h]-xi_group_i[h]) * xi_over_N;
                // Combine the competitive numbers in eps:
                this->eps[h] += xi_final[h];
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
                k1[h] = this->divJ[i][h] - this->dc[i][h] - this->a[i][h] * this->eps[h];
                qq[h] = this->a[i][h] + k1[h] * this->halfdt;
            }

            vector<Flt> k2(this->nhex, 0.0);
            this->compute_divJ (qq, i);
#pragma omp parallel for
            for (unsigned int h=0; h<this->nhex; ++h) {
                k2[h] = this->divJ[i][h] - this->dc[i][h] - qq[h] * this->eps[h];
                qq[h] = this->a[i][h] + k2[h] * this->halfdt;
            }

            vector<Flt> k3(this->nhex, 0.0);
            this->compute_divJ (qq, i);
#pragma omp parallel for
            for (unsigned int h=0; h<this->nhex; ++h) {
                k3[h] = this->divJ[i][h] - this->dc[i][h] - qq[h] * this->eps[h];
                qq[h] = this->a[i][h] + k3[h] * this->dt;
            }

            vector<Flt> k4(this->nhex, 0.0);
            this->compute_divJ (qq, i);

#pragma omp parallel for
            for (unsigned int h=0; h<this->nhex; ++h) {
                k4[h] = this->divJ[i][h] - this->dc[i][h] - qq[h] * this->eps[h];
                this->a[i][h] += (k1[h] + 2.0 * (k2[h] + k3[h]) + k4[h]) * this->sixthdt;
            }

            milliseconds msf5 = duration_cast<milliseconds>(system_clock::now().time_since_epoch());
            this->codetimes.back().a_for4 += (msf5-msf4);

            // Do any necessary computation which involves summing a here
            this->sum_a_computation (i);

            milliseconds msf6 = duration_cast<milliseconds>(system_clock::now().time_since_epoch());
            this->codetimes.back().a_for5 += (msf6-msf5);

            // Now apply the transfer function
//#pragma omp parallel for
            for (unsigned int h=0; h<this->nhex; ++h) {
                this->a[i][h] = this->transfer_a (this->a[i][h], i);
            }

            milliseconds msf7 = duration_cast<milliseconds>(system_clock::now().time_since_epoch());
            this->codetimes.back().a_for6 += (msf7-msf6);
        }
    }

}; // RD_James_dncomp2
