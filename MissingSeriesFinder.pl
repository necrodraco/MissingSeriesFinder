#!/usr/bin/perl

use Getopt::Long;
use IO::Handle; 
use File::Copy "cp"; 
use File::Path "make_path";
use XML::LibXML; 
#use WWW::Mechanize;
use DBI; 

use POSIX "strftime";

use Data::Dumper; 

my $home = '';
my $path   = '';
my $test = 0; 

GetOptions (
	'home=s' => \$home, 
	'path=s' => \$path, 
	'test'   => \$test, 
) or die("Error in command line arguments\n");

if($path ne '' && -e $path && $home ne '' && -e $home){
	my $parser = XML::LibXML->new(); 
	my $source = readXML($parser, $path.'settings.xml'); 

	open (OUTPUT, '>', $source->{'Path_to_Log'}.'missing.log') or die $!;
	STDOUT->fdopen( \*OUTPUT, 'w' ) or die $! if(!$test);

	print 'start: '.getTime();
	my $log = 0;
	$log = 1 if($source->{'LogOption'} eq 'true');

	my $dbh; 
	if($source->{'sql'} == 0){
		$dbh = connectViaMySQL($source); 
	}

	my $sth = $dbh->prepare('
		SELECT 
			t.c00 as seriesName, t.c10 as seriesId, 
		    e.c12 as seasonNumber, e.c13 as episodeNumber
		FROM 
			tvshow t
		JOIN 
			episode e 
		ON 
			t.idShow = e.idShow
		LIMIT 1
	'
	);
	my $worked = $sth->execute();
	
	my %list; 
	if(defined($worked) && $worked ne '0E0'){
		while(my $row = $sth->fetchrow_hashref()){
			my $id = (split(/.xml"/, (split(/cache="/, $row->{'seriesId'}))[1]))[0];
			$id =~ s/\D//g;
			$list{$id}{'name'} = $row->{'seriesName'} if(!defined($list{$id}{'name'}));
			$list{$id}{'episodes'}{'S'.setDigit($row->{'seasonNumber'}).'E'.setDigit($row->{'episodeNumber'})} = 1;
		}
	}
	
	#my $urlReader = WWW::Mechanize->new(); 
	my $found; 
	my $url = "https://thetvdb.com/series/cardfight-vanguard/allseasons/official"; 
	eval{
		$found = $parser->load_html(location => $url);
		print "hier ein\n";
		print Dumper($found);
		print "hier out\n";
	};
	if($@){
		print "Can't connect to Url $url. Series Name is $serie->{'name'}\n";
	#	next; 
	}
	exit();
	print "Ende";
	exit(0);
	while(my ($id, $serie) = each %list){
		my $url = "https://thetvdb.com/series/cardfight-vanguard/allseasons/official"; 
		eval{
			$found = $parser->load_html(location=> $url);
			print "hier ein\n";
			print Dumper($found);
			print "hier out\n";
		};
		if($@){
			print "Can't connect to Url $url. Series Name is $serie->{'name'}\n";
		#	next; 
		}
		exit();
		
		my $dir = $source->{'Path_to_Log'}."MissingSeries/$serie->{'name'}/";
		foreach my $episode(values %{$found->{'Episode'}}){
			my $ename = 'S'.setDigit($episode->{'SeasonNumber'}).'E'.setDigit($episode->{'EpisodeNumber'}); 
			my $count = 1; 
			if(ref($episode->{'EpisodeName'}) eq "HASH"){
				$count = keys %{ $episode->{'EpisodeName'} };			
			}
			next if(
				defined($list{$id}{'episodes'}{$ename})
				|| $count == 0 
				|| $episode->{'EpisodeName'} eq ''
				|| $ename =~ m/E00/
			);
			print "$serie->{'name'}: $ename\n";
			if($log == 1){
				make_path($dir) if( !(-e $dir));
				cp("$home/resources/empty.disc", $dir."$ename.disc") or die 'copy Failed';
			};
			
		}
	}
}else{
	print 'Arguments are not set or false. Please run directly from Kodi Module';
}

print 'finish: '.getTime();

sub setDigit(){
	my ($number) = @_;
	if(length($number) < 2){
		$number = '0'.$number; 
	}
	return $number; 
}

sub getTime(){
	return strftime "%H:%M:%S \n", localtime(time); 
}

sub readXML(){
	my ($parser, $file) = @_; 
	my $dom= $parser->load_xml(location => $file);
	@nodelist = $dom->getElementsByTagName('setting'); 
	my $hash; 
	foreach my $node(@nodelist){
		$hash->{$node->getAttribute("id")} = $node->to_literal();
	}
	return $hash; 
}

sub connectViaMySQL(){
	my ($source) = @_; 
	my (
		$db_host,$db_port, $db_name
	) = (
		$source->{'host'}, 
		$source->{'port'}, 
		$source->{'dbName'}
	);
	return DBI->connect("DBI:mysql:database=$db_name;host=$db_host;port=$db_port", $source->{'username'}, $source->{'password'});
}