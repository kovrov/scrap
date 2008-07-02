#!/usr/bin/perl
use strict;

my $fh = exists $ARGV[0] ? $ARGV[0] : 'datafile';

open(FH, $fh) || die qq/Cannot open <$fh> for reading: "$!"/;

local $/;
$_ = <FH>;

my $h = {};

map push(@{$h->{$_}}, $1), split(/\s+/, substr($2, 1)) while /^(\d+):((?:\s+[A-Z])+)/mg;

print qq/$_: ${\join(' ', sort @{$h->{$_}})}\n/ foreach sort keys %$h;
