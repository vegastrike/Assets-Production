#!/usr/bin/perl

$_ = <>;
print;

while (<>) {
    chomp;
    print;
    if (/^(?:[^,]*,){12}[^,]*([OBAFGKM][\d+.]+)(?:\s(I[abIV]|III|V))?/) {
	$l = $1;
	$l =~ tr/OBAFGKM/1-7/;
	print ",$l";
	if (not defined $2) {
	    print ",1";
	} elsif ($2 eq 'V') {
	    print ",0";
	} else {
	    print ",2";
	}
    } else {
	print ",72,0";
    }
    print "\n";
}
