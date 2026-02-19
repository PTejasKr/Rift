"""
PharmaGuard Merkle Tree Implementation
"""
import hashlib
import json
from typing import List, Optional

class MerkleTree:
    """Merkle tree implementation for product data integrity verification"""
    
    def __init__(self, leaves=None):
        self.leaves = []
        self.tree = []
        self.root = None
        
        if leaves:
            for leaf in leaves:
                self.add_leaf(leaf)
    
    def add_leaf(self, leaf):
        """
        Add a leaf to the merkle tree
        
        Args:
            leaf: The leaf data to add (will be hashed)
        """
        # Hash the leaf if it's not already a hash
        if not isinstance(leaf, str) or len(leaf) != 64:
            leaf = self._hash(leaf)
        
        self.leaves.append(leaf)
        self._build_tree()
    
    def add_leaves(self, leaves):
        """
        Add multiple leaves to the merkle tree
        
        Args:
            leaves: List of leaf data to add
        """
        for leaf in leaves:
            self.add_leaf(leaf)
    
    def get_merkle_root(self):
        """
        Get the merkle root hash
        
        Returns:
            str: The merkle root hash, or None if tree is empty
        """
        return self.root
    
    def get_proof(self, leaf_index):
        """
        Get a merkle proof for a specific leaf
        
        Args:
            leaf_index: Index of the leaf to prove
            
        Returns:
            list: List of sibling hashes forming the proof
        """
        if leaf_index < 0 or leaf_index >= len(self.leaves):
            return []
        
        proof = []
        current_index = leaf_index
        
        for level in range(len(self.tree) - 1):
            level_nodes = self.tree[level]
            is_left = current_index % 2 == 0
            
            if is_left and current_index + 1 < len(level_nodes):
                proof.append({
                    'side': 'right',
                    'hash': level_nodes[current_index + 1]
                })
            elif not is_left:
                proof.append({
                    'side': 'left',
                    'hash': level_nodes[current_index - 1]
                })
            
            current_index = current_index // 2
        
        return proof
    
    def verify_proof(self, leaf, proof, root):
        """
        Verify a merkle proof
        
        Args:
            leaf: The leaf data to verify
            proof: The proof to verify against
            root: The expected merkle root
            
        Returns:
            bool: True if the proof is valid
        """
        current_hash = self._hash(leaf) if not isinstance(leaf, str) or len(leaf) != 64 else leaf
        
        for item in proof:
            if item['side'] == 'left':
                current_hash = self._hash(item['hash'] + current_hash)
            else:
                current_hash = self._hash(current_hash + item['hash'])
        
        return current_hash == root
    
    def get_depth(self):
        """
        Get the depth of the merkle tree
        
        Returns:
            int: The depth of the tree
        """
        return len(self.tree) if self.tree else 0
    
    def get_leaf_count(self):
        """
        Get the number of leaves in the tree
        
        Returns:
            int: Number of leaves
        """
        return len(self.leaves)
    
    def _build_tree(self):
        """Build the merkle tree from the leaves"""
        if not self.leaves:
            self.tree = []
            self.root = None
            return
        
        current_level = self.leaves[:]
        self.tree = [current_level[:]]
        
        while len(current_level) > 1:
            next_level = []
            
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                right = current_level[i + 1] if i + 1 < len(current_level) else left
                
                combined = left + right
                parent_hash = self._hash(combined)
                next_level.append(parent_hash)
            
            self.tree.append(next_level[:])
            current_level = next_level
        
        self.root = current_level[0] if current_level else None
    
    def _hash(self, data):
        """
        Generate SHA-256 hash of data
        
        Args:
            data: Data to hash (string or any serializable type)
            
        Returns:
            str: Hexadecimal hash string
        """
        if isinstance(data, str):
            data = data.encode()
        elif not isinstance(data, bytes):
            data = json.dumps(data, sort_keys=True).encode()
        
        return hashlib.sha256(data).hexdigest()
    
    def to_dict(self):
        """
        Convert merkle tree to dictionary representation
        
        Returns:
            dict: Dictionary containing tree structure
        """
        return {
            'leaves': self.leaves,
            'tree': self.tree,
            'root': self.root,
            'depth': self.get_depth(),
            'leaf_count': self.get_leaf_count()
        }
    
    def __repr__(self):
        return f"MerkleTree(root={self.root}, leaves={len(self.leaves)}, depth={self.get_depth()})"
