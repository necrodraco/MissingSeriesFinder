import xbmcaddon
import xbmcgui

addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
addondir    = xbmc.translatePath( addon.getAddonInfo('path') )
addonsettings    = xbmc.translatePath( addon.getAddonInfo('profile') )

def logging(message): 
    xbmcgui.Dialog().ok(addonname, message)
    xbmc.log(message)

logging("Program MissingSeriesFinder addondir: " + addondir)
logging("Program MissingSeriesFinder addonsettings: " + addonsettings)

command = "perl " + addondir + "/MissingSeriesFinder.pl -home=" + addondir + " -path=" + addonsettings
logging("command: " + command)

#!/usr/bin/perl
#
#use Getopt::Long;
#use IO::Handle; 
#use File::Copy "cp"; 
#use File::Path "make_path";
#use XML::Simple; 
#use WWW::Mechanize;
#use DBI; 
#
#use POSIX "strftime";
#
#my $home = '';
#my $path   = '';#
#
#GetOptions (
#    'home=s' => \$home, 
#    'path=s' => \$path, 
#) or die("Error in command line arguments\n");#
#
#if($path ne '' && -e $path && $home ne '' && -e $home){
#    my $source = XMLin($path.'settings.xml')->{'setting'};
#    
#    open OUTPUT, '>', $source->{'Path_to_Log'}->{'value'}.'missing.log' or die $!;
#    STDOUT->fdopen( \*OUTPUT, 'w' ) or die $!;
#
#    print 'start: '.getTime();
#    my $log = 0;
#    $log = 1 if($source->{'LogOption'}->{'value'} eq 'true');
#
#    my $dbh; 
#    if($source->{'sql'}->{'value'} == 0){
#        
#        my (
#            $db_host,$db_port, $db_name
#        ) = (
#            $source->{'host'}->{'value'}, 
#            $source->{'port'}->{'value'}, 
#            $source->{'dbName'}->{'value'}
#        );
#        
#        $dbh = DBI->connect("DBI:mysql:database=$db_name;host=$db_host;port=$db_port", $source->{'username'}->{'value'}, $source->{'password'}->{'value'});
#    }
#
#    my $sth = $dbh->prepare('
#        SELECT 
#            t.c00 as seriesName, t.c10 as seriesId, 
#            e.c12 as seasonNumber, e.c13 as episodeNumber
#        FROM 
#            tvshow t
#        JOIN 
#            episode e 
#        ON 
#            t.idShow = e.idShow'
#    );
#    my $worked = $sth->execute();
#    
#    my %list; 
#    if(defined($worked) && $worked ne '0E0'){
#        while(my $row = $sth->fetchrow_hashref()){
#            my $id = (split(/.xml"/, (split(/cache="/, $row->{'seriesId'}))[1]))[0];
#            $id =~ s/\D//g;
#            $list{$id}{'name'} = $row->{'seriesName'} if(!defined($list{$id}{'name'}));
#            $list{$id}{'episodes'}{'S'.setDigit($row->{'seasonNumber'}).'E'.setDigit($row->{'episodeNumber'})} = 1;
#        }
#    }
#    
#    my $urlReader = WWW::Mechanize->new(); 
#    my $found = ''; 
#    
#    while(my ($id, $serie) = each %list){
#        my $url = "http://www.thetvdb.com/api/1D62F2F90030C444/series/$id/all/en.xml"; 
#        eval{
#            $found = XMLin($urlReader->get($url)->decoded_content());
#        };
#        if($@){
#            print "Can't connect to Url $url. Series Name is $serie->{'name'}\n";
#            next; 
#        }
#        
#        my $dir = $source->{'Path_to_Log'}->{'value'}."MissingSeries/$serie->{'name'}/";
#        foreach my $episode(values %{$found->{'Episode'}}){
#            my $ename = 'S'.setDigit($episode->{'SeasonNumber'}).'E'.setDigit($episode->{'EpisodeNumber'}); 
#            my $count = 1; 
#            if(ref($episode->{'EpisodeName'}) eq "HASH"){
#                $count = keys %{ $episode->{'EpisodeName'} };           
#            }
#            next if(
#                defined($list{$id}{'episodes'}{$ename})
#                || $count == 0 
#                || $episode->{'EpisodeName'} eq ''
#                || $ename =~ m/E00/
#            );
#            print "$serie->{'name'}: $ename\n";
#            if($log == 1){
#                make_path($dir) if( !(-e $dir));
#                cp("$home/resources/empty.disc", $dir."$ename.disc") or die 'copy Failed';
#            };
#            
#        }
#    }
#}else{
#    print 'Arguments are not set or false. Please run directly from Kodi Module';
#}
#
#print 'finish: '.getTime();
#
#sub setDigit(){
#    my ($number) = @_;
#    if(length($number) < 2){
#        $number = '0'.$number; 
#    }
#    return $number; 
#}
#
#sub getTime(){
#    return strftime "%H:%M:%S \n", localtime(time); 
#}
#