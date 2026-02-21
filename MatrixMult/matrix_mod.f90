! matrix_mod.f90
!
! Compilar con:
! f2py -m matrix_ops -c matrix_mod.f90 --f90flags="-O3 -march=native" -lopenblas

subroutine dot(A, B, C, n)
   implicit none
   integer, intent(in) :: n
   real(8), intent(in) :: A(n, n)
   real(8), intent(in) :: B(n, n)
   !f2py intent(inout) C  ! Directiva especial para F2PY
   real(8), intent(out) :: C(n, n)
   real(8) :: alpha, beta
   external dgemm

   alpha = 1.0_8
   beta  = 0.0_8

   ! Multiplicación de matrices utilizando DGEMM (BLAS)
   call dgemm('N', 'N', n, n, n, alpha, A, n, B, n, beta, C, n)

end subroutine dot
