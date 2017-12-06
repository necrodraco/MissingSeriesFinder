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

if($path ne '' && -e $path ){
	print 'path is '.(Dumper $path);

	my $xmlReader = XmlReader->new();

	my $source = $xmlReader->read($path.'settings.xml')->{'setting'};
	print Dumper $source;
	my $sql; 
	if($source->{'sql'}->{'value'} == 0){
		$sql = SqlManager->new(
			'host' => $source->{'host'}->{'value'}, 
			'port' => $source->{'port'}->{'value'}, 
			'dbname' => $source->{'dbName'}->{'value'}, 
			'user' => $source->{'username'}->{'value'}, 
			'pass' => $source->{'password'}->{'value'}, 
		);
		$sql->connect();
	}
	my $list = $sql->getSeries();
	print Dumper $list; 

	my $list2 = ();
	while(my ($id, $serie) = each %{$list}){
		my $content = $xmlReader->readFromXml('http://www.thetvdb.com/api/1D62F2F90030C444/series/'.$id.'/all/en.xml');
		print Dumper $content; 
	}
}else{
	print 'Arguments are not set or false. Please run directly from Kodi Module';
}