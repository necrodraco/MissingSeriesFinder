#!/usr/bin/perl

package XmlReader{
	use Moose; 
	use XML::Simple; 
	use WWW::Mechanize; 

	use lib 'lib';
	extends 'Library'; 

	has 'xml' => ('is' => 'rw', );
	has 'bot' => ('is' => 'rw', 'default' => sub{WWW::Mechanize->new()});
	sub read(){
		my ($self, $file) = @_;
		$self->xml(XMLin($file));
		return $self->xml();
	}

	sub readFromXml(){
		my ($self, $url) = @_;
		my $found = $self->read(
			$self->bot()
				->get($url)
				->decoded_content()
		);
		my $serie->{$found->{'Series'}->{'id'}}->{'name'} = $found->{'Series'}->{'SeriesName'}; 
		while(my ($key, $episode) = each %{$found->{'Episode'}}){
			$serie->{$found->{'Series'}->{'id'}}->{'episodes'}->{'S'.$self->setDigit($episode->{'SeasonNumber'}).'E'.$self->setDigit($episode->{'EpisodeNumber'})} = 1;
		}
		return $serie; 
	}
}
1; 