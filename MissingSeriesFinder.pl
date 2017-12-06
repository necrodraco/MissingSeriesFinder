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
	
	my $list2 = ();
	while(my ($id, $serie) = each %{$list}){
		my $content = $xmlReader->readFromXml('http://www.thetvdb.com/api/1D62F2F90030C444/series/'.$id.'/all/en.xml');
		$list2->{$id} = $content->{$id};
	}

	my $missing = (); 
	while(my ($id2, $serie2) = each %{$list2}){
		my $episodes = $list->{$id2}->{'episodes'};
		my $episodes2 = $serie2->{'episodes'}; 
		while(my ($episode, $stat) = each %{$episodes2}){
			if(!defined($episodes->{$episode})){
				$missing->{$serie2->{'name'}}->{$episode} = 1; 
			}
		}
	}
	print 'Missing: '.(Dumper $missing); 
}else{
	print 'Arguments are not set or false. Please run directly from Kodi Module';
}