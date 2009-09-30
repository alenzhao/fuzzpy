#!/usr/bin/env python

"""\
Unit tests for FuzzPy.

@author: Aaron Mavrinac
@organization: University of Windsor
@contact: mavrin1@uwindsor.ca
@license: GPL-3
"""

import unittest

import fuzz
print "FuzzPy imported from '%s'" % fuzz.__path__[ 0 ]


class TestFuzzyGraph( unittest.TestCase ):
    
    def setUp( self ):
        v = set( [ 1, 2, 3, 4, 5 ] )
        self.D = fuzz.FuzzyGraph( viter = v, directed = True )
        self.U = fuzz.FuzzyGraph( viter = v, directed = False )
        for G in [ self.U, self.D ]:
            G.connect( 1, 2, 0.8 )
            G.connect( 2, 3, 1.0 )
            G.connect( 3, 4, 0.9 )
            G.connect( 4, 5, 0.7 )
            G.connect( 3, 5, 0.2 )
            G.connect( 5, 2, 0.5 )
            G.connect( 1, 5, 0.0 )

    def test_vertices( self ):
        exp = set( [ 1, 2, 3, 4, 5 ] )
        act = self.U.vertices
        self.assertEqual( act, exp )

    def test_mu( self ):
        exp = [ 0., 0.7, 0.7, 0. ]
        act = [ self.U.mu( 1, 3 ),
                self.U.mu( 4, 5 ),
                self.U.mu( 5, 4 ),
                self.D.mu( 5, 4 ) ]
        self.assertEqual( act, exp )

    def test_weight( self ):
        exp = [ 0., 1., float( 'inf' ), 1. / 0.9, 1. / 0.9, float( 'inf' ) ]
        act = [ self.U.weight( 1, 1 ),
                self.U.weight( 2, 3 ),
                self.U.weight( 1, 5 ),
                self.D.weight( 3, 4 ),
                self.U.weight( 4, 3 ),
                self.D.weight( 4, 3 ) ]
        self.assertEqual( act, exp )

    def test_adjacent( self ):
        act = True
        act &= self.D.adjacent( 1, 2 )
        act &= not self.D.adjacent( 2, 1 )
        act &= self.U.adjacent( 1, 2 )
        act &= self.U.adjacent( 2, 1 )
        self.assert_( act )

    def test_connected( self ):
        act = True
        act &= self.D.connected( 1, 5 )
        act &= not self.D.connected( 5, 1 )
        act &= self.U.connected( 1, 5 )
        act &= self.U.connected( 5, 1 )
        self.assert_( act )

    def test_dijkstra_directed( self ):
        exp = { 1 : None, 2 : 1, 3 : 2, 4 : 3, 5 : 4 }
        act = self.D.dijkstra( 1 )
        self.assertEqual( act, exp )

    def test_dijkstra_undirected( self ):
        exp = { 1 : None, 2 : 1, 3 : 2, 4 : 3, 5 : 2 }
        act = self.U.dijkstra( 1 )
        self.assertEqual( act, exp )

    def test_shortest_path_directed( self ):
        ep = [ 1, 2, 3, 4, 5 ]
        el = 0.
        for i in range( len( ep ) - 1 ):
            el += self.D.weight( ep[ i ], ep[ i + 1 ] )
        act = self.D.shortest_path( 1, 5 )
        self.assertEqual( act, ( ep, el ) )

    def test_shortest_path_undirected( self ):
        ep = [ 1, 2, 5 ]
        el = 0.
        for i in range( len( ep ) - 1 ):
            el += self.U.weight( ep[ i ], ep[ i + 1 ] )
        act = self.U.shortest_path( 1, 5 )
        self.assertEqual( act, ( ep, el ) )

    def test_floyd_warshall_directed( self ):
        exp = self.D.shortest_path( 1, 5 )[ 1 ]
        act = self.D.floyd_warshall()[ 1 ][ 5 ]
        self.assertEqual( act, exp )

    def test_floyd_warshall_undirected( self ):
        exp = self.U.shortest_path( 1, 5 )[ 1 ]
        act = self.U.floyd_warshall()[ 1 ][ 5 ]
        self.assertEqual( act, exp )


if __name__ == '__main__':
    unittest.main()
