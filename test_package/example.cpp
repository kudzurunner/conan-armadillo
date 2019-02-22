#include <iostream>
#include <armadillo>

int main() {
    std::cout << "arma version: " << arma::arma_version::as_string() << std::endl;

    arma::mat A = arma::randu<arma::mat>(2,3);
    A.print("A=");

    arma::mat B;
    B << 0.1 << 0.2 << 0.3 << arma::endr
      << 0.4 << 0.5 << 0.6 << arma::endr;
    B.print("B=");

    arma::mat C = A + 3.0 * B;
    C.print("C=");

    C.save("c_mat.h5", arma::hdf5_binary);
    return 0;
}
