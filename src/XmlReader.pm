#!/usr/bin/perl

package XmlReader{
	use Moose; 
	use XML::Simple; 

	has 'xml' => ('is' => 'rw', );

	sub read(){
		my ($self, $file) = @_;
		$self->xml(XMLin($file));
	}
}
1; 