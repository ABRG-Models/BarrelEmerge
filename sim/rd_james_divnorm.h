/*
 * 2D Karbowski system with *divisive* normalization of a_i, deriving
 * from RD_James base class.
 */

#include "rd_james.h"

//! Use the normalization method in which we account for those branches which have
//! made connections (see supp.tex. 2020/01/24)
#define SUBTRACT_C_FROM_A 1

template <class Flt>
class RD_James_divnorm : public RD_James<Flt>
{
public:

    /*!
     * An N element vector holding the sum of a_i for each TC type.
     */
    alignas(vector<Flt>) vector<Flt> sum_a;

    /*!
     * An N element vector holding the initial sum of a_i for each TC type.
     */
    alignas(vector<Flt>) vector<Flt> sum_a_init;

#ifdef SUBTRACT_C_FROM_A
    /*!
     * An N element vector holding the sum of c_i for each TC type.
     */
    alignas(vector<Flt>) vector<Flt> sum_c;
#endif

    /*!
     * Simple constructor; no arguments. Just calls base constructor.
     */
    RD_James_divnorm (void)
        : RD_James<Flt>() {
    }

    virtual void allocate (void) {
        RD_James<Flt>::allocate();
        this->resize_vector_param (this->sum_a, this->N);
        this->resize_vector_param (this->sum_a_init, this->N);
#ifdef SUBTRACT_C_FROM_A
        this->resize_vector_param (this->sum_c, this->N);
#endif
    }

    virtual void init (void) {
        RD_James<Flt>::init();
        // Now compute sum of a and record this as sum_a_init.
        for (unsigned int i = 0; i < this->N; ++i) {
            this->sum_a_computation(i);
        }
        this->sum_a_init = this->sum_a;
#if 0
        // Print these on screen
        for (unsigned int ii = 0; ii < this->sum_a_init.size(); ++ii) {
            cout << "sum_a_init["<<ii<<"] = " << this->sum_a_init[ii] << endl;
        }
#endif
    }

    /*!
     * Computation methods
     */
    //@{

    /*!
     * A possibly normalization-function specific task to carry out
     * once after the sum of a has been computed.
     */
    virtual void sum_a_computation (const unsigned int _i) {
        // Compute the sum of a[i] across the sheet.
        this->sum_a[_i] = 0.0;
        Flt sum_tmp = 0.0;
#pragma omp parallel for reduction(+:sum_tmp)
        for (unsigned int h=0; h<this->nhex; ++h) {
            sum_tmp += this->a[_i][h];
        }
        this->sum_a[_i] = sum_tmp;

#ifdef SUBTRACT_C_FROM_A
        // Compute the sum of c[i] across the sheet.
        this->sum_c[_i] = 0.0;
        sum_tmp = 0.0;
#pragma omp parallel for reduction(+:sum_tmp)
        for (unsigned int h=0; h<this->nhex; ++h) {
            sum_tmp += this->c[_i][h];
        }
        this->sum_c[_i] = sum_tmp;
#endif
    }

    /*!
     * The normalization/transfer function.
     */
    virtual inline Flt transfer_a (const Flt& _a, const unsigned int _i) {
#if defined NORMALIZE_TO_ONE
        // Divisive normalization to one
        Flt a_rtn = this->nhex * _a / this->sum_a[_i];
#elif defined SUBTRACT_C_FROM_A
        Flt a_rtn = (this->sum_a_init[_i] - this->sum_c[_i]) * _a / this->sum_a[_i];
#else
        // Divisive norm with initial sum multiplier
        Flt a_rtn = this->sum_a_init[_i] * _a / this->sum_a[_i];
#endif
        // Prevent a from becoming negative, necessary only when competition is implemented:
        return (a_rtn < 0.0) ? 0.0 : a_rtn;
    }

}; // RD_James_norm
