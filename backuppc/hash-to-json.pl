#!/usr/bin/perl
# A cli tool I wanted to use outputted a perl hash as a string.
# This reads it in from stdin, and returns json instead.
use JSON;
my @lines = <STDIN>;

my %Status;  # TODO: Unhard-code this.
eval $lines[0]; #TODO: handle multiple lines?

my $json = encode_json \%Status;
print $json;
