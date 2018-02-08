from array import *
import numpy as np
from scipy.stats import gaussian_kde
import sys

def get_data(pairings_filename):
	positive_alignments = array('f', [])
	negative_alignments = array('f', [])

	with open(pairings_filename, "r") as in_file:
		for line in in_file:
			line = line.rstrip("\n").split(",")
			
			if line[0] == "p":
				positive_alignments.append(float(line[1]))
			elif line[0] == "n":
				negative_alignments.append(float(line[1]))

	return positive_alignments, negative_alignments

def pair_list_and_write_to_file(filename, ec, x_vals, y_vals):
	with open(filename, "a") as out:
		zipped_vals = zip(x_vals, y_vals)

		out.writelines(",".join([ec, ",".join(str(val)[1:-1].split(", ")) + "\n"]) for val in zipped_vals)

def estimate_density(qec, pairings_filename, density_pos_filename, density_neg_filename):
	print("Estimating density function for " + qec)

	X_pos, X_neg = get_data(pairings_filename)

	X_pos_len, X_neg_len = len(X_pos), len(X_neg)

	if X_pos_len > 1:
		X_min, X_max = min(X_pos), max(X_pos)
		X_plot = np.linspace(X_min, X_max, 1500)
		kde = gaussian_kde(X_pos, bw_method='silverman')
		dens = kde.evaluate(X_plot)
		pair_list_and_write_to_file(density_pos_filename, qec, X_plot, dens)

	if X_neg_len > 2:
		X_min, X_max = min(X_neg), max(X_neg)
		X_plot = np.linspace(X_min, X_max, 1500)
		kde = gaussian_kde(X_neg, bw_method='silverman')
		dens = kde.evaluate(X_plot)
		pair_list_and_write_to_file(density_neg_filename, qec, X_plot, dens)

	print("Finished estimating density function for " + qec)

def main():
	serial_num = sys.argv[2]
	density_pos_filename, density_neg_filename = "density-pos." + serial_num + ".out", "density-neg." + serial_num + ".out"

	ec = sys.argv[1]
	pairings_filename = ec + '_aligned_unique_pairs.txt'
	estimate_density(ec, pairings_filename, density_pos_filename, density_neg_filename)

	with open("processed." + serial_num + ".txt", "a") as processed:
		processed.write(ec + "\n")

if __name__ == "__main__":
	main()
