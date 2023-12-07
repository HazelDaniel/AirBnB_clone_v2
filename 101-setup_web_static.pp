# deploy static recreation of task 0
$static_dirs = [ '/data/', '/data/web_static/',
                        '/data/web_static/releases/', '/data/web_static/shared/',
                        '/data/web_static/releases/test/'
                  ]

package {'nginx':
  ensure  => installed,
}

file { $static_dirs:
        ensure  => 'directory',
        owner   => 'ubuntu',
        group   => 'ubuntu',
        recurse => 'remote',
        mode    => '0766',
}

file { '/data/web_static/current':
  ensure  => link,
  target  => '/data/web_static/releases/test/',
  require => File[$static_dirs[1]],
}

file {'/data/web_static/releases/test/index.html':
  ensure  => present,
  content => "<html>\n\t<head>\n\t</head>\n\t<body>\n\t\tHolberton School\n\t</body>\n</html>",
  require => File['/data/web_static/current']
}

exec { 'changing ownership of /data':
  command => 'chown -R ubuntu:ubuntu /data/',
  path    => '/usr/bin/:/usr/local/bin/:/bin/',
}

file_line {'deploy static':
  path  => '/etc/nginx/sites-available/default',
  after => 'server_name _;',
  line  => "\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t\tindex.html index.html;\n\t}",
}

service {'nginx':
  ensure  => running,
}

exec {'/etc/init.d/nginx restart':
}
