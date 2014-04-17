#!/usr/bin/env python
from nose.tools import assert_equal, assert_true
import numpy as np
import pandas as p
from Bio import SeqIO
from concoct.input import _normalize_per_sample, _normalize_per_contig, generate_feature_mapping, load_composition

class TestInput(object):
    def setUp(self):
        self.C = p.DataFrame(np.array([[0., 0.7], [5.5, .7]]))

    def test_normalize_per_contig(self):
        C_norm = _normalize_per_contig(self.C)
        
        C_correct = p.DataFrame(np.array([[0., 1.],[5.5/6.2, 0.7/6.2]]))
        assert_true(np.linalg.norm(C_norm-C_correct) < 0.0001)

    def test_normalize_per_samples(self):
        C_norm = _normalize_per_sample(self.C)

        C_correct = p.DataFrame(np.array([[0., 0.5],[1,0.5]]))
        assert_true(np.linalg.norm(C_norm-C_correct) < 0.0001)

    def test_generate_feature_mapping(self):
        feature_mapping, counter = generate_feature_mapping(2)
        assert_equal(counter, 10)
        assert_equal(len(feature_mapping.keys()), 16)
        assert_true('AA' in feature_mapping)

    def test_load_composition(self):
        seqs = SeqIO.parse("test_data/composition_some_shortened.fa","fasta")
        ids = []
        lengths = []
        for s in seqs:
            ids.append(s.id)
            lengths.append(len(s))
        c_len = p.Series(lengths,index=ids,dtype=float)

        composition,contig_lengths,threshold_filter = load_composition("test_data/composition_some_shortened.fa",4,1000)
        assert_true((c_len == contig_lengths).all())