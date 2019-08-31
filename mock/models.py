import uuid

from django.db.models import BooleanField, CASCADE, CharField, DateTimeField, ForeignKey, PositiveIntegerField, Model, \
    UUIDField
from django.urls import reverse
from django.utils import timezone


class Mock(Model):
    user = ForeignKey('auth.User', on_delete=CASCADE)
    status = ForeignKey('mock.Status', on_delete=CASCADE)
    title = CharField(max_length=128, unique=True)
    response_body = CharField(max_length=4096)
    mock_path = UUIDField(default=uuid.uuid4, unique=True)
    create_date = DateTimeField(default=timezone.now)
    is_active = BooleanField(default=True)
    call_no = PositiveIntegerField(default=0)

    def get_absolute_url(self):
        return reverse('mock:mock_list')

    def __str__(self):
        return self.title


class Status(Model):
    class Meta:
        verbose_name_plural = "status"

    status_code = PositiveIntegerField(primary_key=True)
    reason = CharField(max_length=128)
    descriprion = CharField(max_length=4096)

    def __str__(self):
        return str(self.status_code) + ' ' + self.reason


class ResponseHeader(Model):
    mock = ForeignKey('mock.Mock', on_delete=CASCADE)
    tag = CharField(max_length=4096)
    value = CharField(max_length=4096)
    is_standard = BooleanField(default=False)

    STANDARD_HEADER_TAGS = ['Accept-Patch', 'Accept-Ranges', 'Age', 'Allow', 'Alt-Svc', 'Cache-Control', 'Connection',
                            'Content-Disposition', 'Content-Encoding', 'Content-Language', 'Content-Length',
                            'Content-Location', 'Content-Range', 'Content-Type', 'Date', 'Delta-Base', 'ETag',
                            'Expires', 'IM', 'Last-Modified', 'Link', 'Location', 'Pragma', 'Proxy-Authenticate',
                            'Public-Key-Pins', 'Retry-After', 'Server', 'Set-Cookie', 'Strict-Transport-Security',
                            'Trailer', 'Transfer-Encoding', 'Tk', 'Upgrade', 'Vary', 'Via', 'Warning',
                            'WWW-Authenticate']

    STANDARD_HEADER_PLACEHOLDERS = ["text/example;charset=utf-8", "bytes", "12", "GET, HEAD",
                                    'http/1.1= "http2.example.com:8001"; ma=7200',
                                    "max-age=3600 / no-cache, no-store, max-age=0, must-revalidate", "close",
                                    'attachment; filename="file.txt"', "gzip", "en", "348", "/index.htm",
                                    "bytes 21010-47021/47022", "text/html; charset=utf-8",
                                    "Tue, 15 Nov 1994 08:12:31 GMT", '"abc"', '"737060cd8c284d8a[...]"',
                                    "Sat, 01 Dec 2018 16:00:00 GMT", "feed", "Mon, 15 Nov 2017 12:00:00 GMT",
                                    '</feed>; rel="alternate"', "/pub/WWW/People.html", "no-cache", "Basic", "",
                                    "120 / Fri, 07 Nov 2014 23:59:59 GMT", "Apache/2.4.1 (Unix)",
                                    "UserID=JohnDoe; Max-Age=3600; Version=1", "max-age=16070400; includeSubDomains",
                                    "Max-Forwards", "chunked", "?", "h2c, HTTPS/1.3, IRC/6.9, RTA/x11, websocket",
                                    "Accept-Language / *", "1.0 fred, 1.1 example.com (Apache/1.1)",
                                    "199 Miscellaneous warning", "Basic"]

    STANDARD_HEADER_DESCRIPTIONS = ["Specifies which patch document formats this server supports.",
                                    "What partial content range types this server supports via byte serving.",
                                    "The age the object has been in a proxy cache in seconds.",
                                    "Valid methods for a specified resource. To be used for a 405 Method not allowed.",
                                    "A server uses “Alt-Svc” header (meaning Alternative Services) to indicate that its resources can also be accessed at a different network location (host or port) or using a different protocol. When using HTTP/2, servers should instead send an ALTSVC frame.",
                                    "If no-cache is used, the Cache-Control header can tell the browser to never use a cached version of a resource without first checking the ETag value. max-age is measured in seconds. The more restrictive no-store option tells the browser (and all the intermediary network devices) the not even store the resource in its cache.",
                                    "Control options for the current connection and list of hop-by-hop response fields. Deprecated in HTTP/2.",
                                    "An opportunity to raise a “File Download” dialogue box for a known MIME type with binary format or suggest a filename for dynamic content. Quotes are necessary with special characters.",
                                    "The type of encoding used on the data. See HTTP compression.",
                                    "The natural language or languages of the intended audience for the enclosed content.",
                                    "The length of the response body expressed in 8-bit bytes.",
                                    "An alternate location for the returned data.",
                                    "Where in a full body message this partial message belongs.",
                                    "The MIME type of this content.",
                                    "The date and time that the message was sent (in “HTTP-date” format as defined by RFC 7231).",
                                    "Specifies the delta-encoding entity tag of the response.",
                                    "An identifier for a specific version of a resource, often a message digest.",
                                    "Gives the date/time after which the response is considered stale (in “HTTP-date” format as defined by RFC 7231).",
                                    "Instance-manipulations applied to the response.",
                                    "The last modified date for the requested object (in “HTTP-date” format as defined by RFC 7231).",
                                    "Used to express a typed relationship with another resource, where the relation type is defined by RFC 5988.",
                                    "Used in redirection, or when a new resource has been created.",
                                    "Implementation-specific fields that may have various effects anywhere along the request-response chain..",
                                    "Request authentication to access the proxy.",
                                    "HTTP Public Key Pinning, announces hash of website’s authentic TLS certificate.",
                                    "If an entity is temporarily unavailable, this instructs the client to try again later. Value could be a specified period of time (in seconds) or a HTTP-date.",
                                    "A name for the server.", "An HTTP cookie.",
                                    "A HSTS Policy informing the HTTP client how long to cache the HTTPS only policy and whether this applies to subdomains.",
                                    "The Trailer general field value indicates that the given set of header fields is present in the trailer of a message encoded with chunked transfer coding.",
                                    "The form of encoding used to safely transfer the entity to the user. Currently defined methods are: chunked, compress, deflate, gzip, identity. Deprecated in HTTP/2.",
                                    "Tracking Status header, value suggested to be sent in response to a DNT(do-not-track), possible values: “!” — under construction “?” — dynamic “G” — gateway to multiple parties “N” — not tracking “T” — tracking “C” — tracking with consent “P” — tracking only if consented “D” — disregarding DNT “U” — updated.",
                                    "Ask the client to upgrade to another protocol. Deprecated in HTTP/2.",
                                    "Tells downstream proxies how to match future request headers to decide whether the cached response can be used rather than requesting a fresh one from the origin server.",
                                    "Informs the client of proxies through which the response was sent.",
                                    "A general warning about possible problems with the entity body.",
                                    "Indicates the authentication scheme that should be used to access the requested entity."]

    def __str__(self):
        return str(self.mock) + ' ' + self.tag


class StandardResponseHeader(Model):
    tag = CharField(max_length=4096)
    placeholder = CharField(max_length=4096)
    description = CharField(max_length=4096)

    def __str__(self):
        return self.tag


class Request(Model):
    mock = ForeignKey('mock.Mock', on_delete=CASCADE)
    method = ForeignKey('mock.Method', on_delete=CASCADE)
    host = CharField(max_length=256)
    port = PositiveIntegerField()
    path = CharField(max_length=2048)
    scheme = CharField(max_length=16)
    body = CharField(max_length=4096)
    timestamp = DateTimeField(default=timezone.now)
    req_path = UUIDField(default=uuid.uuid4, unique=True)
    req_no = PositiveIntegerField()

    def __str__(self):
        return str(self.mock) + ' ' + str(self.timestamp)


class RequestHeader(Model):
    request = ForeignKey('mock.Request', on_delete=CASCADE)
    tag = CharField(max_length=4096)
    value = CharField(max_length=4096)

    def __str__(self):
        return str(self.request) + ' ' + self.tag


class Method(Model):
    method = CharField(max_length=8)

    def __str__(self):
        return self.method


class Parameter(Model):
    request = ForeignKey('mock.Request', on_delete=CASCADE)
    tag = CharField(max_length=2048)
    is_post = BooleanField(default=False)

    def __str__(self):
        return str(self.request) + ' ' + self.tag


class ParameterValue(Model):
    parameter = ForeignKey('mock.Parameter', on_delete=CASCADE)
    value = CharField(max_length=2048)

    def __str__(self):
        return str(self.parameter) + ' ' + self.value


class Cookie(Model):
    request = ForeignKey('mock.Request', on_delete=CASCADE)
    tag = CharField(max_length=4096)
    value = CharField(max_length=4096)

    def __str__(self):
        return str(self.request) + ' ' + self.tag


class UserPermission(Model):
    mock = ForeignKey('mock.Mock', on_delete=CASCADE)
    user = ForeignKey('auth.User', on_delete=CASCADE)

    def __str__(self):
        return str(self.mock) + ' ' + str(self.user)
