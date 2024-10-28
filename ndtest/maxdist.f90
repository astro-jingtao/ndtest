subroutine maxdist(x1, y1, sort1, x2, y2, sort2, n1, n2, D_max)
    implicit none
    integer, intent(in) :: n1, n2, sort1(n1), sort2(n2)
    real, intent(in) :: x1(n1), y1(n1), x2(n2), y2(n2)
    real, intent(inout) :: D_max
    integer :: i_indx1, i_indx2
    real :: this_y1
    logical :: ly1(n1), ly2(n2)
    real :: a1, b1, c1, d1, a2, b2, c2, d2, D(4)

    D_max = 0
    i_indx2 = 0


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

        ! see Press, William H. Numerical recipes 3rd edition: The art of scientific computing. Cambridge university press, 2007. Section 14.8 for 1/real(n1) term.
        D = [(a1 - a2 - 1/real(n1)), (b1 - b2), (c1 - c2), (d1 - d2)]
        D_max = max(D_max, maxval(D) + 1/real(n1), -minval(D))
    end do

    ! write(*,*) D_max

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