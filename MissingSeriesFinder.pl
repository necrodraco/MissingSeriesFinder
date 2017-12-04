#!/usr/bin/perl

use Data::Dumper; 
use Getopt::Long;

use lib 'lib';
use SqlManager; 
use XmlReader; 

my $path   = '';
GetOptions (
	'path=s' => \$path, 
) or die("Error in command line arguments\n");

print 'path is '.(Dumper $path);

my $xmlReader = XmlReader->new();

my $source = $xmlReader->read($path.'settings.xml');
print Dumper $source;
print Dumper $source->{'setting'}->{'host'};
my $sql = SqlManager->new(

);