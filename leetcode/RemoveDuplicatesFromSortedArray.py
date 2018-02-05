class Solution(object):
    def removeDuplicates(self,nums):
        """
        :param nums: list[int]
        :return:
        """
        if not nums:
            return 0
        removed_end = 0
        for i in range(1,len(nums)):
            if nums[i] != nums[removed_end]:
                removed_end += 1
                nums[removed_end] = nums[i]

        return removed_end + 1

if __name__ == '__main__':
    nums = [1, 2, 3, 4, 4, 5, 5, 6]
    soloution = Solution()
    print(soloution.removeDuplicates(nums))
    print(nums)