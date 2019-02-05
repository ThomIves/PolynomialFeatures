class Poly_Features_Pure_Py:
    def __init__(self, order=2, interaction_only=False, include_bias=True):
        """
        Mimics sklearn's PolyFeatures class to create various orders and types
        of polynomial variables from an initial set of supplied variables.
            :param order: the order of polynomials to be used - default is 2
            :param interaction_only: this means that only those polynomials
                with interaction, and that would add up in total power to the 
                given order, will be created for the set of polynomials. The
                default value is false.
            :param include_bias: the bias term is the one constant term in the
                final polynomial series. The default is to include it - True.
                To NOT include it, set this to False.
        """       
        self.order = order
        self.interaction_only = interaction_only
        self.include_bias = include_bias
            
        # Called to make sure all parameters have been correctly set
        self.__check_for_param_errors__()
        
    def fit(self, X):
        """
        Based on parameters and values of X, determine a set of powers 
        for each variable in the given X. This function only finds a list
        of powers that are needed. Transform applies those powers to the 
        lists of variables provided.
            :param X: a list of lists containing the values for which to 
                create power for.
        """

        # Make sure X is of the correct format.
        self.__check_X_is_list_of_lists__(X)

        # Determine the number of variables and create the initial 
        #   form of the powers list
        self.vars = len(X[0])
        self.powers = [0]*self.vars

        # Establish parameters and call the routine that gets the different
        #   combinations of powers needed for the order.
        order = self.order
        powers = self.powers
        self.__get_powers_lists__(order=order, 
            var=1, 
            powers=powers, 
            powers_lists=set())

        # Once all power combinations have been found, sort them.
        self.powers_lists.sort(reverse=True)

        # Eliminate powers not needed based on initialization parameters.
        self.__modify_powers_lists__()

    def get_feature_names(self, default_names=[]):
        """
        Routine to present the powers obtained from fit in an algebraic text format
            :param default_names: If this list is not empty, the text provided will
                be used in place of the default style of x0, x1, x2, ... xn
        """

        # Section 1: creates default names if not provided.
        if len(default_names) == 0:
            for i in range(self.vars):
                default_names.append('x' + str(i))
        # if default names are provided, makes sure they are of correct form
        elif len(default_names) != self.vars:
            err_str = 'Provide exactly {} feature names.'.format(self.vars)
            raise ValueError(err_str)
        elif len(default_names) == self.vars:
            check = [x for x in default_names if type(x) == str]
            if len(check) != self.vars:
                err_str = 'All feature names must be type string.'
                raise ValueError(err_str)

        # Section 2: Creates the features names based on the 
        #   default base feature names. 
        feature_names = []
        for powers in self.powers_lists:
            prod = []
            for i in range(len(default_names)):
                if powers[i] == 0:
                    continue
                elif powers[i] == 1:
                    val = default_names[i]
                else: 
                    val = default_names[i] + '^' + str(powers[i])
                prod.append(val)
            if prod == []:
                prod = ['1']
            feature_names.append(' '.join(prod))
        
        return feature_names

    def transform(self, X):
        """
        Apply the lists of powers previously found from fit to the provided
        arrays of X values
            :param X: The provided array of lists of input / feature values
        """   

        # Make sure X is of the correct format.
        self.__check_X_is_list_of_lists__(X)

        # Apply the powers found previously in fit to X
        Xout = []
        for row in X:
            temp = []
            for powers in self.powers_lists:
                prod = 1
                for i in range(len(row)):
                    prod *= row[i] ** powers[i]
                temp.append(prod)
            Xout.append(temp)

        return Xout
        
    def fit_transform(self, X):
        """
        Simlpy calls fit and transform in one step for convenience.
            :param X: The provided array of lists of input / feature values
        """   
        # Make sure X is of the correct format.
        self.__check_X_is_list_of_lists__(X)

        self.fit(X)
        return self.transform(X)

    def get_params(self):
        """
        Simply collects and returns the current parameter values in a 
        dictionary format
        """
        tmp_dict = {'order':self.order,
                    'interaction_only':self.interaction_only,
                    'include_bias':self.include_bias}

        print(tmp_dict)

    def set_params(self, **kwargs):
        """
        Allows user to provide keyword argument inputs to change parameters.
            :param **kwargs: keyword argument pairs are converted to 
                dictionary format
        """   
        if 'order' in kwargs:
            self.order = kwargs['order']
        if 'interaction_only' in kwargs:
            self.interaction_only = kwargs['interaction_only']
        if 'include_bias' in kwargs:
            self.include_bias = kwargs['include_bias']
            
        # Called to make sure all parameters have been correctly set
        self.__check_for_param_errors__()

    def __get_powers_lists__(self, order=2, var=1, powers=[0,0], powers_lists=set()):
        """
        Called from fit to obtain a set of power arrays for all instances of all 
        features. 
            :param order: default of 2 and used to set highest order
            :param var: current feature variable being worked on 
            :param powers: the current state of the powers array that will be 
                added to the list of powers
            :param powers_lists: the full set of powers lists
        """
        for pow in range(order+1):
            powers[var-1] = pow
            if sum(powers) <= order:
                powers_lists.add(tuple(powers))
            if var < self.vars:
                self.__get_powers_lists__(order=order, 
                    var=var+1, 
                    powers=powers, 
                    powers_lists=powers_lists)

        # Convert all tuples to lists for operational convenience
        self.powers_lists = [list(x) for x in powers_lists]

    def __modify_powers_lists__(self):
        """
        A private method to modify the powers lists based on the input parameters
        """
        # If only interactive combinations are desired, eliminate those features 
        
        #   that aren't interactive
        if self.interaction_only == True:
            self.powers_lists = [
                x for x in self.powers_lists if sum(x) == self.order]
        
        # If no bias is desired, remove it
        if self.include_bias == False:
            try:
                self.powers_lists.remove([0]*self.vars)
            except:
                pass

    def __check_for_param_errors__(self):
        """
        Simple method to ensure input parameters are of the correct type
        """
        error_string = ''
        if type(self.order) != int:
            error_string += '"order" needs to be of type int. '
        if type(self.interaction_only) != bool:
            error_string += '"interaction_only" needs to be of type bool. '
        if type(self.include_bias) != bool:
            error_string += '"include_bias" needs to be of type bool. '

        if error_string != '':
            raise TypeError(error_string)

    def __check_X_is_list_of_lists__(self, X):
        """
        Simple method to make sure that X input is of the correct format
        """
        error_string = 'X must be a list of lists.'
        if type(X) != list:
            raise TypeError(error_string)
        if type(X[0]) != list:
            raise TypeError(error_string)
        

import LinearAlgebraPurePython as la 

###############################################################################

max_range = 2

X = [[1*x for x in range(max_range)],
     [2*x for x in range(max_range)]]

X = la.transpose(X) 
la.print_matrix(X)
print()

my_poly = Poly_Features_Pure_Py(order=2)
my_poly.fit(X)

feature_names = my_poly.get_feature_names()
feature_names.sort()
print(feature_names)
print()

wxMax = ['x1^2', 'x0 x1', 'x1', 'x0^2', 'x0', '1']
wxMax.sort()
sklearn_poly_features = ['1', 'x0', 'x0 x1', 'x0^2', 'x1', 'x1^2']
sklearn_poly_features.sort()

if wxMax == feature_names == sklearn_poly_features:
    print("Output from sklearn's PolynomialFeatures and from wxMaxima match the above.")


###############################################################################
import sys
sys.exit()

X = la.transpose(X) 
la.print_matrix(X)
print()

my_poly = Poly_Features_Pure_Py(order=3)
my_poly.get_params()
my_poly.set_params(include_bias=False)
my_poly.get_params()

my_poly.fit(X)

print(len(my_poly.powers_lists))
feature_names = my_poly.get_feature_names() # ['v','w','x','y','z']
feature_names.sort()
print(feature_names)
print()
#######

my_poly.set_params(interaction_only=True)
my_poly.get_params()

my_poly.fit(X)

print(len(my_poly.powers_lists))
feature_names = my_poly.get_feature_names()
feature_names.sort()
print(feature_names)
print()
#######

my_poly.set_params(interaction_only=False, include_bias=True)
my_poly.get_params()

my_poly.fit(X)

print(len(my_poly.powers_lists))
feature_names = my_poly.get_feature_names()
feature_names.sort()
print(feature_names)
print()


# if feature_names == ['1', 'x0', 'x0 x1', 'x0 x1 x2', 'x0 x1 x3', 'x0 x1 x4', 'x0 x1^2', 'x0 x2', 'x0 x2 x3', 'x0 x2 x4', 'x0 x2^2', 'x0 x3', 'x0 x3 x4', 'x0 x3^2', 'x0 x4', 'x0 x4^2', 'x0^2', 'x0^2 x1', 'x0^2 x2', 'x0^2 x3', 'x0^2 x4', 'x0^3', 'x1', 'x1 x2', 'x1 x2 x3', 'x1 x2 x4', 'x1 x2^2', 'x1 x3', 'x1 x3 x4', 'x1 x3^2', 'x1 x4', 'x1 x4^2', 'x1^2', 'x1^2 x2', 'x1^2 x3', 'x1^2 x4', 'x1^3', 'x2', 'x2 x3', 'x2 x3 x4', 'x2 x3^2', 'x2 x4', 'x2 x4^2', 'x2^2', 'x2^2 x3', 'x2^2 x4', 'x2^3', 'x3', 'x3 x4', 'x3 x4^2', 'x3^2', 'x3^2 x4', 'x3^3', 'x4', 'x4^2', 'x4^3']:
#     print(True)

# Xout = my_poly.transform(X)
# la.print_matrix(Xout)
# print('[1, 4, 8, 12, 16, 20, 16, 32, 48, 64, 80, 64, 96. 128, 160, 144, 192, 240, 256, 320, 400]')
# print()

# Xout = my_poly.fit_transform(X)
# la.print_matrix(Xout)

