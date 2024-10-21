#import ctypes

class Array:    
    def __init__(self, size=0): # O(1)
        self._elements = [None]*size
        self._size = size

    # Creates an array with size elements.
    #def __init__( self, size=0 ):
    #  assert size >= 0, "Array size must be >= 0"
      #print("Initializing an array of size ", size)
    #  self._size = size
    #  # Create the array structure using the ctypes module.
    #  PyArrayType = ctypes.py_object * size
    #  self._elements = PyArrayType()
    #  # Initialize each element.
    #  self.clear( 0)    

    def __len__(self): return self._size # O(1)
    def __iter__(self): yield from self._elements # O(n) iter_seq

    def build(self, X): # O(n)
        self._elements = [a for a in X] # pretend this builds a static array
        self._size = len(self._elements)
        
        
    def get_at(self, index): 
        assert index >= 0 and index < len(self), "Array subscript out of range"
        return self._elements[index] # O(1)
        

    def set_at(self, index, value): 
       assert index >= 0 and index < len(self), "Array subscript out of range"
       self._elements[ index ] =value    # O(1)

    def _copy_forward(self, i, n, A, j): # O(n)
        """Copies self._elements[i:i+n] to A[j:j+n]."""
        for k in range(n):
            A.set_at(j + k , self._elements[i + k])

    def _copy_backward(self, i, n, A, j): # O(n)
        """ Copies self._elements[i:i+n] to A[j:j+n] starting from the 
        last element and moving backwards.
        """
        for k in range(n - 1, -1, -1):
            A.set_at(j + k, self._elements[i + k])

    def insert_at(self, i, x): # O(n)
        n = len(self)
        A = [None]* (n+1)
        self._copy_forward(0, i, A, 0)
        A[i] = x
        self._copy_forward(i, n - i, A, i + 1)
        self.build(A)

    def delete_at(self, i): # O(n)
        n = len(self)
        A = [None] * (n - 1)
        self._copy_forward(0, i, A, 0)
        x = self._elements[i]
        self._copy_forward(i + 1, n - i - 1, A, i)
        self.build(A)
        return x
        # O(n)

    def insert_first(self, x): self.insert_at(0, x)
    def delete_first(self): return self.delete_at(0)
    def insert_last(self, x): self.insert_at(len(self), x)
    def delete_last(self): return self.delete_at(len(self) - 1)


   # Gets the contents of the index element.
   # def __getitem__( self, index ):
   #     return self.get_at(self,index)
   
 

   # Puts the value in the array element at index position.
   # def __setitem__( self, index, value ):
   #     return self.set_at( self, index, value )
      

   # Clears the array by setting each element to the given value.
    def clear( self, value ):
      for i in range( len(self) ) :
         self._elements.set_at(i , value)

   # Returns the array's iterator for traversing the elements.
      #def __iter__( self ):
      #   return _ArrayIterator( self._elements )





class Dynamic_Array:
    def __init__(self, r = 2): # O(1)
        super().__init__()
        self._elements=Array()
        self._size = 0
        self.r = r  # resizing factor
        self._compute_bounds()
        self._resize(0)

    def __len__(self): return self._size # O(1)

    def __iter__(self): # O(n)
        for i in range(len(self)): yield self._elements.get_at(i)


    def get_at(self, index): 
        assert index >= 0 and index < len(self), "Array subscript out of range"
        return self._elements.get_at(index) # O(1)
        

    def set_at(self, index, value): 
       assert index >= 0 and index < len(self), "Array subscript out of range"
       self._elements.set_at( index ,value )   # O(1)    
    
    def build(self, X): # O(n)
        for a in X: self.insert_last(a)
        
    
    def _compute_bounds(self): # O(1)
        self.upper = len(self._elements)   # The current capacity of the dynamic array

        # The capacity of the dynamic array divided by the square of the resize factor (here 4)
        # used for deciding when to shrink the array after a series of item deletions.
        self.lower = len(self._elements) // (self.r * self.r) 

    def _resize(self, n): # O(1) or O(n)
        if (self.lower < n < self.upper): return
        
        m = max(n, 1) * self.r # New capacity
        A = Array(m)
        self._elements._copy_forward(0, self._size, A, 0)
        self._elements = A
        self._compute_bounds()
    
    def insert_last(self, x): # O(1)a
        self._resize(self._size + 1)
        self._elements.set_at(self._size, x)
        self._size += 1
    
    def delete_last(self): # O(1)a
        self._elements.set_at(self._size - 1 , None)
        self._size -= 1
        self._resize(self._size)
    
    def insert_at(self, i, x): # O(n)
        self.insert_last(None)
        self._elements._copy_backward(i, self._size - (i + 1), self._elements, i + 1)
        self.A[i] = x
    
    def delete_at(self, i): # O(n)
        x = self._elements.get_at(i)
        self._elements._copy_forward(i + 1, self._size - (i + 1), self._elements, i)
        self.delete_last()
        return x # O(n)

    def insert_first(self, x): self.insert_at(0, x)
    def delete_first(self): return self.delete_at(0)