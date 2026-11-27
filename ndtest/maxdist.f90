! Largest difference between the empirical distribution functions of two samples, with the points of the first sample as origins.
! The points are visited in the order of their x coordinate. Two Fenwick trees over the y ranks hold the points with an x coordinate up to the current one, one tree per sample, so that every quadrant count is a sum over the ranks up to the rank of the origin.
subroutine maxdist(x1, sort1, rank1, x2, sort2, rank2, n1, n2, D_max)
    implicit none
    integer, intent(in) :: n1, n2, sort1(n1), sort2(n2), rank1(n1), rank2(n2)
    real, intent(in) :: x1(n1), x2(n2)
    real, intent(inout) :: D_max(1)
    integer :: i_indx1, i_indx2, i_end, i, j, k, m, below1, below2, this_rank
    integer :: rank1_sorted(n1), rank2_sorted(n2)
    integer, allocatable :: tree1(:), tree2(:), cum1(:), cum2(:)
    real :: x0
    real :: a1, b1, c1, d1, a2, b2, c2, d2, D(4)

    ! the ranks in the x order of their sample
    rank1_sorted = rank1(sort1)
    rank2_sorted = rank2(sort2)
    m = max(maxval(rank1_sorted), maxval(rank2_sorted))

    ! cum(k) is the number of points of a sample with a rank up to k
    allocate (cum1(m), cum2(m), tree1(m), tree2(m))
    cum1 = 0
    cum2 = 0
    do k = 1, n1
        cum1(rank1_sorted(k)) = cum1(rank1_sorted(k)) + 1
    end do
    do k = 1, n2
        cum2(rank2_sorted(k)) = cum2(rank2_sorted(k)) + 1
    end do
    do k = 2, m
        cum1(k) = cum1(k) + cum1(k - 1)
        cum2(k) = cum2(k) + cum2(k - 1)
    end do
    ! the trees start empty: no point is inserted yet
    tree1 = 0
    tree2 = 0

    D_max(1) = 0
    ! i_indx2 points of sample 2 and i_end points of sample 1 are in the trees
    i_indx2 = 0
    i_end = 0

    do i_indx1 = 1, n1
        x0 = x1(sort1(i_indx1))

        ! i_indx2 is the number of sample-2 points with x2 <= x0
        do while ((i_indx2 < n2) .and. (x2(sort2(i_indx2 + 1)) <= x0))
            i_indx2 = i_indx2 + 1
            i = rank2_sorted(i_indx2)
            do while (i <= m)
                tree2(i) = tree2(i) + 1
                i = i + iand(i, -i)
            end do
        end do

        ! i_end is the last point of sample 1 with the x of the current point: the quadrant x <= x0
        ! holds the whole tie group, whichever member of the group is the origin
        if (i_indx1 > i_end) then
            i_end = i_indx1
            do while ((i_end < n1) .and. (x1(sort1(i_end + 1)) == x0))
                i_end = i_end + 1
            end do
            do j = i_indx1, i_end
                i = rank1_sorted(j)
                do while (i <= m)
                    tree1(i) = tree1(i) + 1
                    i = i + iand(i, -i)
                end do
            end do
        end if

        ! below is the number of inserted points with a rank up to the rank of the origin
        this_rank = rank1_sorted(i_indx1)
        below1 = 0
        i = this_rank
        do while (i > 0)
            below1 = below1 + tree1(i)
            i = i - iand(i, -i)
        end do
        below2 = 0
        i = this_rank
        do while (i > 0)
            below2 = below2 + tree2(i)
            i = i - iand(i, -i)
        end do

        ! write(*,*) x0
        call quadct(i_end, below1, cum1(this_rank), n1, a1, b1, c1, d1)
        ! write(*,*) n1, a1, b1, c1, d1, a1 + b1 + c1 + d1

        call quadct(i_indx2, below2, cum2(this_rank), n2, a2, b2, c2, d2)
        ! write(*,*) n2, a2, b2, c2, d2, a2 + b2 + c2 + d2

        ! see Press, William H. Numerical recipes 3rd edition: The art of scientific computing. Cambridge university press, 2007. Section 14.8 for 1/real(n1) term.
        D = [(a1 - a2 - 1/real(n1)), (b1 - b2), (c1 - c2), (d1 - d2)]
        D_max(1) = max(D_max(1), maxval(D) + 1/real(n1), -minval(D))
    end do

    ! write(*,*) D_max

end subroutine

! i_indx points of a sample lie in x <= x0, below of them in y <= y0, and below_all points of the sample lie in y <= y0.
subroutine quadct(i_indx, below, below_all, n, a, b, c, d)
    implicit none
    integer, intent(in) :: i_indx, below, below_all, n
    real, intent(out) :: a, b, c, d

    a = real(below) / real(n)
    b = real(i_indx) / real(n) - a
    c = real(below_all - below) / real(n)
    d = 1 - real(i_indx) / real(n) - c
end subroutine
