program heat_equation
   implicit none
   integer :: N, timesteps
   real(8) :: a2, tau, a, b, dx, pi
   integer :: i, j, s
   real(8), allocatable :: x(:), u0(:), u_prev(:), u_new(:), G(:,:)
   character(len=32) :: arg
   character(len=*), parameter :: filename = "Datos/u_sol.txt"

   ! Leer argumentos de la línea de comandos
   call get_command_argument(1, arg)
   read(arg, *) a2
   call get_command_argument(2, arg)
   read(arg, *) tau
   call get_command_argument(3, arg)
   read(arg, *) a
   call get_command_argument(4, arg)
   read(arg, *) b
   call get_command_argument(5, arg)
   read(arg, *) N
   call get_command_argument(6, arg)
   read(arg, *) timesteps

   ! Calcular constantes
   pi = 4.0d0 * atan(1.0d0)
   dx = (b - a) / (2*N)

   ! Reservar memoria
   allocate(x(2*N+1), u0(2*N+1), u_prev(2*N+1), u_new(2*N+1), G(2*N+1, 2*N+1))

   ! Crear vector de posición
   do i = 1, 2*N+1
       x(i) = a + dx * (i - 1)
   end do

   ! Guardar vector de posición en x.txt
   open(unit=11, file="Datos/x.txt", status="replace")
   do i = 1, 2*N+1
       write(11, '(F12.8)', advance='no') x(i)
       if (i < 2*N+1) write(11, '(A)', advance='no') ' '
   end do
   write(11,*) ''
   close(11)

   ! Guardar parámetros de la simulación en sim.txt
   open(unit=12, file="Datos/sim.txt", status="replace")
   write(12, '(A,F10.6)') "a2 = ", a2
   write(12, '(A,F10.6)') "tau = ", tau
   write(12, '(A,F10.6)') "a = ", a
   write(12, '(A,F10.6)') "b = ", b
   write(12, '(A,I10)') "N = ", N
   write(12, '(A,I10)') "timesteps = ", timesteps
   close(12)

   ! Condición inicial
   u0 = 0.0
   do i = 1, 2*N+1
       if (x(i) > -0.25d0 .and. x(i) < 0.25d0) then
           u0(i) = 0.1d0
       end if
   end do
   u_prev = u0

   ! Calcular matriz G
   do i = 1, 2*N+1
       do j = 1, 2*N+1
           G(i,j) = (dx / sqrt(4.0d0 * pi * a2 * tau)) * exp(-(dx**2 / (4.0d0 * a2 * tau)) * (i - j)**2)
       end do
   end do

   ! Abrir archivo para escritura
   open(unit=10, file=filename, status="replace")

   ! Guardar u0
   do j = 1, 2*N+1
       write(10, '(F10.6)', advance='no') u0(j)
       if (j < 2*N+1) write(10, '(A)', advance='no') ' '
   end do
   write(10,*) ''

   ! Evolución temporal
   do s = 1, timesteps - 1
       u_new = 0.0d0
       do i = 1, 2*N+1
           do j = 1, 2*N+1
               u_new(i) = u_new(i) + G(i,j) * u_prev(j)
           end do
       end do
       do j = 1, 2*N+1
           write(10, '(F10.6)', advance='no') u_new(j)
           if (j < 2*N+1) write(10, '(A)', advance='no') ' '
       end do
       write(10,*) ''
       u_prev = u_new
   end do

   close(10)

end program heat_equation