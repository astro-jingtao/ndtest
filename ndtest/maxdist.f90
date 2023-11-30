subroutine maxdist(x1, y1, sort1, x2, y2, sort2, n1, n2, D_max)
    implicit none
    integer, intent(in) :: n1, n2, sort1(n1), sort2(n2)
    real, intent(in) :: x1(n1), y1(n1), x2(n2), y2(n2)
    real, intent(inout) :: D_max
    integer :: i_indx1, i_indx2
    real :: this_y1
    logical :: ly1(n1), ly2(n2)
    real :: a1, b1, c1, d1, a2, b2, c2, d2, D(4)

    ! call argsort(x1,n1,sort1)
    ! call argsort(x2,n2,sort2)
    D_max = 0
    i_indx2 = 0

    ! write(*,*) "sort1", sort1

    do i_indx1 = 1, n1
        ! i_indx2 指向最大的小于等于 x1[sort1[i_indx1]] 的元素
        do while ((i_indx2 < n2).and.(x2(sort2(i_indx2+1)) <= x1(sort1(i_indx1))))
            i_indx2 = i_indx2 + 1
        end do
        
        this_y1 = y1(sort1(i_indx1))

        ly1 = y1 <= this_y1
        ly2 = y2 <= this_y1

        ! write(*,*) x1(sort1(i_indx1))
        call quadct(ly1, sort1, i_indx1, n1, a1, b1, c1, d1)
        ! write(*,*) n1, a1, b1, c1, d1, a1 + b1 + c1 + d1

        call quadct(ly2, sort2, i_indx2, n2, a2, b2, c2, d2)
        ! write(*,*) n2, a2, b2, c2, d2, a2 + b2 + c2 + d2

        D = [(a1 - a2 - 1/real(n1)), (b1 - b2), (c1 - c2), (d1 - d2)]
        D_max = max(D_max, maxval(D) + 1/real(n1), -minval(D))
    end do
end subroutine

subroutine quadct(ly, sort, i_indx, n, a, b, c, d)
    implicit none
    logical, intent(in) :: ly(n)
    integer, intent(in) :: sort(n), i_indx, n
    real, intent(out) :: a, b, c, d

    a = real(count(ly(sort(1:i_indx)))) / real(n)
    b = real(i_indx) / real(n) - a
    c = real(count(ly(sort(i_indx+1:n)))) / real(n)
    d = 1 - real(i_indx)/ real(n) - c
end subroutine

! ! 速度瓶颈在这里
! subroutine argsort(arr,n,indx)
!     implicit none
!     integer, intent(in) :: n
!     real, intent(in) :: arr(n)
!     integer, intent(out) :: indx(n)
!     integer :: i, j
!     integer :: temp
!     do i = 1, n
!         indx(i) = i
!     end do
!     do i = 1, n-1
!         do j = i+1, n
!             if (arr(indx(j)) < arr(indx(i))) then
!                 temp = indx(i)
!                 indx(i) = indx(j)
!                 indx(j) = temp
!             end if
!         end do
!     end do
! end subroutine