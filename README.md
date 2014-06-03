quincy
======

> "If you want to get the answers, talk to Quincy ..."

![Quincy](images/quincy.jpg)

Just like the famous forensic pathologist, you can talk to Quincy to ask
questions of StackTach.v3. "How happened to this instance?" "How did it die?"
"Who touched it last?" "Was it in pain?"

Quincy is a REST interface for StackTach.v3 ... but it's only the API, there
is no implementation. The default implementation is a dummy one for testing
purposes. You can specify different implementations as you like. So, if
you have another monitoring service that you would like to expose with a
StackTach.v3 interface, you can adopt Quincy. However, if you want to work with
StackTach.v3, there is a [quince](https://github.com/StackTach/quince) driver 
that handles that for you.

Later in this document we will show you how to configure Quincy to use 
the Quince drivers.

The [klugman](https://github.com/StackTach/klugman) library is both a cmdline 
tool for accessing `quincy` and a python library for programmatically accessing it. 
