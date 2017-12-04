#!/usr/bin/perl

use Data::Dumper; 
use Getopt::Long;

use lib 'src';
use SqlManager; 
use XmlReader; 

my $path   = '';
GetOptions (
	'path=s' => \$path, 
) or die("Error in command line arguments\n");

print 'path is '.(Dumper $path);

my $xmlReader = XmlReader->new();

$xmlReader->read('./addon.xml');

#my $sql = SqlManager->new();