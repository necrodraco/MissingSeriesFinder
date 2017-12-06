#!/usr/bin/perl

package Library{
	use Moose; 

	sub setDigit(){
		my ($self, $number) = @_;
		if(length($number) < 2){
			$number = '0'.$number; 
		}
		return $number; 
	}
}
1; 