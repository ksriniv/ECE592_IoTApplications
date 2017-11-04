# This file is part of the Python aiocoap library project.
#
# Copyright (c) 2012-2014 Maciej Wasilak <http://sixpinetrees.blogspot.com/>,
#               2013-2014 Christian Amsüss <c.amsuess@energyharvesting.at>
#
# aiocoap is free software, this file is published under the MIT license as
# described in the accompanying LICENSE file.

"""This module provides interface base classes to various aiocoap services,
especially with respect to request and response handling."""

import abc
from asyncio import coroutine

class TransportEndpoint(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    @coroutine
    def shutdown(self):
        """Deactivate the complete transport, usually irrevertably. When the
        coroutine returns, the object must have made sure that it can be
        destructed by means of ref-counting or a garbage collector run."""

    @abc.abstractmethod
    def send(self, message):
        """Send a given :class:`Message` object"""

    @abc.abstractmethod
    @coroutine
    def fill_remote(self, message):
        """Populate a message's remote property based on its .opt.uri_host or
        .unresolved_remote. This interface is likely to change."""

class RequestProvider(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def request(self, request_message):
        """Create and act on a a :class:`Request` object that will be handled
        according to the provider's implementation."""

class Request(metaclass=abc.ABCMeta):
    """A CoAP request, initiated by sending a message. Typically, this is not
    instanciated directly, but generated by a :meth:`RequestProvider.request`
    method."""

    response = """A future that is present from the creation of the object and \
        fullfilled with the response message."""

class Resource(metaclass=abc.ABCMeta):
    """Interface that is expected by a :class:`.protocol.Context` to be present
    on the serversite, which renders all requests to that context."""

    @abc.abstractmethod
    @coroutine
    def render(self, request):
        """Return a message that can be sent back to the requester.

        This does not need to set any low-level message options like remote,
        token or message type; it does however need to set a response code.

        The ``aiocoap.message.NoResponse`` sentinel can be returned if the
        resources wishes to suppress an answer on the request/response
        layer. (An empty ACK is sent responding to a CON request on message
        layer nevertheless.)"""

    @abc.abstractmethod
    @coroutine
    def needs_blockwise_assembly(self, request):
        """Indicator to the :class:`.protocol.Responder` about whether it
        should assemble request blocks to a single request and extract the
        requested blocks from a complete-resource answer (True), or whether
        the resource will do that by itself (False)."""

class ObservableResource(Resource, metaclass=abc.ABCMeta):
    """Interface the :class:`.protocol.ServerObservation` uses to negotiate
    whether an observation can be established based on a request.

    This adds only functionality for registering and unregistering observations;
    the notification contents will be retrieved from the resource using the
    regular :meth:`.render` method from crafted (fake) requests.
    """
    @abc.abstractmethod
    @coroutine
    def add_observation(self, request, serverobservation):
        """Before the incoming request is sent to :meth:`.render`, the
        :meth:`.add_observation` method is called. If the resource chooses to
        accept the observation, it has to call the
        `serverobservation.accept(cb)` with a callback that will be called when
        the observation ends. After accepting, the ObservableResource should
        call `serverobservation.trigger()` whenever it changes its state; the
        ServerObservation will then initiate notifications by having the
        request rendered again."""
