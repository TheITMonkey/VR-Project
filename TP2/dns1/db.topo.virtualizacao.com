;
; BIND data file for local loopback interface
;
$TTL	604800
@	IN	SOA	dns1.topo.virtualizacao.com. admin.topo.virtualizacao.com. (
			      3		; Serial
			 604800		; Refresh
			  86400		; Retry
			2419200		; Expire
			 604800 )	; Negative Cache TTL
;

;name servers - NS records
IN		NS		dns1.topo.virtualizacao.com.
IN		NS		dns2.topo.virtualizacao.com.

;name servers - A records
dns1.topo.virtualizacao.com.		IN		A		192.168.3.1
dns2.topo.virtualizacao.com.		IN		A		192.168.3.2


; 192.168.0.0/16 - A records
fileserver1.topo.virtualizacao.com.		IN		A		192.168.1.1
fileserver2.topo.virtualizacao.com.		IN		A		192.168.1.2
cliente1.topo.virtualizacao.com.	IN		A		192.168.2.1
cliente2.topo.virtualizacao.com.	IN		A		192.168.2.2