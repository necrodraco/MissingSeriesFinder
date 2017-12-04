#!/usr/bin/perl

package SqlManager{
	use Moose; 
	use DBI; 

	has 'dbh' => ('is' => 'rw', );
	has 'user' => ('is' => 'rw', 'required' => 1, );
	has 'pass' => ('is' => 'rw', 'required' => 1, );

	sub connect(){
		my ($self) = @_;
		$self->dbh(DBI->connect(
			"DBI:mysql:database=bring_m_backalive;"."host=localhost", 
			$self->user(), 
			$self->pass(), 
		));
	}
}
1; 