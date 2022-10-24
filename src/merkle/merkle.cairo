//TODO: Clean this up and refactor the create_merkle_tree monstrosity

// calculate merkle root of a merkle tree out of bitcoin block hashes
from starkware.cairo.common.math import unsigned_div_rem
from starkware.cairo.common.math_cmp import is_le_felt
from starkware.cairo.common.pow import pow
from starkware.cairo.common.cairo_builtins import HashBuiltin
from starkware.cairo.common.hash import hash2
from starkware.cairo.common.math import assert_le

//##
//
//           Create a Merkle tree over block headers
//       1. Block headers are hashed with Pedersen
//       2. hashes are stored in array
//       3. calculate the Merkle root
//           -> in every level the previous hashes are sorted before hashed (a < b <=> hash(a,b))
//           -> if a sub-tree is missing a second entry to calculate the parent hash
//              it will just return the current hash
//               e.g.
//
//                   A              A              A
//                 /   \          /   \         /     \
//                B     C        B     5       B       C
//               / \    |       / \    |      / \    /   \
//              D   E   C      C   D   5     D   E   F   7
//             / \ / \ / \    / \ / \  |    / \ / \ / \  |
//             1 2 3 4 5 6    1 2 3 4  5    1 2 3 4 5 6  7
//##

// start with left_index = 0 and right_index is 2**Height-1
// -> can calc the height with a hint
func create_merkle_tree{pedersen_ptr: HashBuiltin*, range_check_ptr}(
    leaves_ptr: felt*, left_index: felt, leaves_ptr_len: felt, height: felt
) -> (root: felt) {
    alloc_locals;
    if (height == 0) {
        return (leaves_ptr[left_index],);
    }
    let (curr1) = create_merkle_tree(leaves_ptr, left_index, leaves_ptr_len, height - 1);
    let (interval_size) = pow(2, height);
    let right_index = left_index + interval_size - 1;
    let (right_subtree_left_index, _) = unsigned_div_rem(left_index + right_index, 2);

    let out_of_bounds = is_le_felt(leaves_ptr_len, right_subtree_left_index + 1);
    if (out_of_bounds == 1) {
        return (curr1,);
    } else {
        let (curr2) = create_merkle_tree(
            leaves_ptr, right_subtree_left_index + 1, leaves_ptr_len, height - 1
        );
    }

    let le = is_le_felt(curr1, curr2);

    if (le == 1) {
        let (n) = hash2{hash_ptr=pedersen_ptr}(curr1, curr2);
        let root = n;
    } else {
        let (n) = hash2{hash_ptr=pedersen_ptr}(curr2, curr1);
        let root = n;
    }
    return (root,);
}

func calculate_height{range_check_ptr}(len) -> felt {
    alloc_locals;
    local height: felt;
    %{
        import math
        ids.height = math.ceil(math.log2(ids.len))
    %}
    // check that the calculated height is correct
    // len > 2**(h-1)
    if (height == 0) {
        tempvar range_check_ptr = range_check_ptr;
    } else {
        let (len_lower_bound) = pow(2, height - 1);
        assert_le(len_lower_bound, len - 1);
        tempvar range_check_ptr = range_check_ptr;
    }
    // len <= 2 ** h
    let (len_upper_bound) = pow(2, height);
    assert_le(len, len_upper_bound);

    return height;
}
