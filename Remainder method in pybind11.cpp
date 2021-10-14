////file name : test.cpp

/*
c++ -O3 -Wall -shared -std=c++11 -undefined dynamic_lookup $(python3 -m pybind11 --includes) test.cpp -o test_cpp$(python3-config --extension-suffix) -I /usr/local/Cellar/eigen/3.3.9/include/eigen3
*/

#include <iostream>
#include <string>
#include <pybind11/pybind11.h>
#include <pybind11/eigen.h>
#include <Eigen/Core>
#include <cmath>
using namespace std;
using namespace Eigen;




typedef Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> Matrix;


MatrixXd remainder1(MatrixXd  m, double z) {
/*
    //m = m.unaryExpr([=](const double x){return remainder(x, z) ;});
    m = m.unaryExpr([=](const double x){return
    remainder( (remainder(x, z) + z ), z ) ;});
*/
    m = m.unaryExpr([=](const double x){return fmod(x, z) ;});
    m = m*(255/z);
    return m;
}


/*
int main(){
    Eigen::MatrixXd mat(2,2) ,B ;
    double z = 0.3;
    mat << 2,3,4,5;
    
    //B = mat.unaryExpr([=](const double x){return remainder(x, z) ;});
    cout << mat << endl;
    cout << remainder1(mat, z)<<endl;
    return 0;
}
*/
PYBIND11_MODULE(test_cpp, m){
    m.doc() = "this is test";
    m.def ("remainder1", &remainder1,"remainder");
}

