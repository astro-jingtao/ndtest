subroutine maxdist(x1, y1, sort1, x2, y2, sort2, n1, n2, D_max)
    implicit none
    integer, intent(in) :: n1, n2, sort1(n1), sort2(n2)
    real, intent(in) :: x1(n1), y1(n1), x2(n2), y2(n2)
    real, intent(inout) :: D_max(1)
    integer :: i_indx1, i_indx2, i_end
    real :: this_y1
    real :: y1_sorted(n1), y2_sorted(n2)
    real :: a1, b1, c1, d1, a2, b2, c2, d2, D(4)

    D_max(1) = 0
    i_indx2 = 0
    i_end = 0
    ! the y coordinates in the x order of their sample: quadct then counts over contiguous sections
    y1_sorted = y1(sort1)
    y2_sorted = y2(sort2)


    do i_indx1 = 1, n1
        ! i_indx2 is the number of sample-2 points with x2 <= x1(sort1(i_indx1))
        do while ((i_indx2 < n2).and.(x2(sort2(i_indx2+1)) <= x1(sort1(i_indx1))))
            i_indx2 = i_indx2 + 1
        end do

        ! i_end is the last point of sample 1 with the x of the current point: the quadrant x <= x1
        ! holds the whole tie group, whichever member of the group is the origin
        if (i_indx1 > i_end) then
            i_end = i_indx1
            do while ((i_end < n1).and.(x1(sort1(i_end+1)) == x1(sort1(i_indx1))))
                i_end = i_end + 1
            end do
        end if

        this_y1 = y1_sorted(i_indx1)

        ! write(*,*) x1(sort1(i_indx1))
        call quadct(y1_sorted, n1, i_end, this_y1, a1, b1, c1, d1)
        ! write(*,*) n1, a1, b1, c1, d1, a1 + b1 + c1 + d1

        call quadct(y2_sorted, n2, i_indx2, this_y1, a2, b2, c2, d2)
        ! write(*,*) n2, a2, b2, c2, d2, a2 + b2 + c2 + d2

        ! see Press, William H. Numerical recipes 3rd edition: The art of scientific computing. Cambridge university press, 2007. Section 14.8 for 1/real(n1) term.
        D = [(a1 - a2 - 1/real(n1)), (b1 - b2), (c1 - c2), (d1 - d2)]
        D_max(1) = max(D_max(1), maxval(D) + 1/real(n1), -minval(D))
    end do

    ! write(*,*) D_max

end subroutine

subroutine quadct(y, n, i_indx, y_thresh, a, b, c, d)
    implicit none
    integer, intent(in) :: n, i_indx
    real, intent(in) :: y(n)
    real, intent(in) :: y_thresh
    real, intent(out) :: a, b, c, d
    logical :: ly(n)

    ly = y <= y_thresh
    a = real(count(ly(1:i_indx))) / real(n)
    b = real(i_indx) / real(n) - a
    c = real(count(ly(i_indx+1:n))) / real(n)
    d = 1 - real(i_indx)/ real(n) - c
end subroutine