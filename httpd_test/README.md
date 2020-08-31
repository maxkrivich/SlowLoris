# Testing

```bash
# Run web-server + exploit
$ docker-compose up -d
# Check logs
$ docker-compose exec web_server bash -c "tail -f /var/log/httpd/*log"
```