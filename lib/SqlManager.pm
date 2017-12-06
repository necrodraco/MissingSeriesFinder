#!/usr/bin/perl

package SqlManager{
	use Moose; 
	use DBI; 
	use lib 'lib'; 
	extends 'Library'; 

	has 'dbh' => ('is' => 'rw', );
	has 'host' => ('is' => 'rw', 'required' => 1, );
	has 'port' => ('is' => 'rw', 'required' => 1, );
	has 'dbname' => ('is' => 'rw', 'required' => 1, );
	has 'user' => ('is' => 'rw', 'required' => 1, );
	has 'pass' => ('is' => 'rw', 'required' => 1, );

	sub connect(){
		my ($self) = @_;
		my ($db_host, $db_port, $db_name, $db_user, $db_pass) = 
		($self->host(), $self->port(), $self->dbname(), $self->user(), $self->pass());
		$self->dbh(
			DBI->connect(
					"DBI:mysql:database=$db_name;host=$db_host;port=$db_port", $db_user, $db_pass
				),
		);
	}

	sub getSeries(){
		my ($self) = @_; 
		my $sth = $self->dbh()->prepare('
			SELECT 
				t.c00 as seriesName, t.c12 as seriesId, 
			    e.c12 as seasonNumber, e.c13 as episodeNumber
			FROM 
				tvshow t
			JOIN 
				episode e 
			ON 
				t.idShow = e.idShow
			where t.c12 = 259640
		');

		my $worked = $sth->execute();
		
		my $series = (); 

		if(defined($worked) && $worked ne '0E0'){
			while(my $row = $sth->fetchrow_hashref()){
				#$series->{$row->{'seriesId'}}->{'name'} = $row->{'seriesName'};
				$series->{$row->{'seriesId'}}->{'episodes'}->{'S'.$self->setDigit($row->{'seasonNumber'}).'E'.$self->setDigit($row->{'episodeNumber'})} = 1;
			}
		}

		return $series; 
	}
}
1; 