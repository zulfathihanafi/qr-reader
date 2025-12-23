### To build
`docker build -t qr-extractor .`

### To run

```
docker run --rm \
  -v $(pwd):/data \
  qr-extractor /data/{filename}.pdf 
```
