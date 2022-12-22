# -*- coding: utf-8 -*- #
# Copyright 2022 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Commands for interacting with the Cloud NetApp Files Storage Pool API resource."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from apitools.base.py import list_pager
from googlecloudsdk.api_lib.netapp.constants import OPERATIONS_COLLECTION
from googlecloudsdk.api_lib.netapp.constants import STORAGE_POOL_RESOURCE
from googlecloudsdk.api_lib.netapp.util import GetClientInstance
from googlecloudsdk.api_lib.netapp.util import GetMessagesModule
from googlecloudsdk.api_lib.netapp.util import VERSION_MAP
from googlecloudsdk.api_lib.util import waiter
from googlecloudsdk.calliope import base
from googlecloudsdk.core import log
from googlecloudsdk.core import resources


class StoragePoolsClient(object):
  """Wrapper for working with Storage Pool in the Cloud NetApp Files API Client.
  """

  def __init__(self, release_track=base.ReleaseTrack.ALPHA):
    if release_track == base.ReleaseTrack.ALPHA:
      self._adapter = AlphaStoragePoolsAdapter()
    else:
      raise ValueError('[{}] is not a valid API version.'.format(
          VERSION_MAP[release_track]))

  @property
  def client(self):
    return self._adapter.client

  @property
  def messages(self):
    return self._adapter.messages

  def WaitForOperation(self, operation_ref):
    """Waits on the long-running operation until the done field is True.

    Args:
      operation_ref: the operation reference.

    Raises:
      waiter.OperationError: if the operation contains an error.

    Returns:
      the 'response' field of the Operation.
    """
    return waiter.WaitFor(
        waiter.CloudOperationPollerNoResources(
            self.client.projects_locations_operations), operation_ref,
        'Waiting for [{0}] to finish'.format(operation_ref.Name()))

  def CreateStoragePool(self, storagepool_ref, async_, config):
    """Create a Cloud NetApp Storage Pool."""
    request = self.messages.NetappProjectsLocationsStoragePoolsCreateRequest(
        parent=storagepool_ref.Parent().RelativeName(),
        storagePoolId=storagepool_ref.Name(),
        storagePool=config)
    create_op = self.client.projects_locations_storagePools.Create(request)
    if async_:
      return create_op
    operation_ref = resources.REGISTRY.ParseRelativeName(
        create_op.name, collection=OPERATIONS_COLLECTION)
    return self.WaitForOperation(operation_ref)

  def ParseStoragePoolConfig(self,
                             name=None,
                             service_level=None,
                             capacity=None,
                             description=None,
                             labels=None):
    """Parses the command line arguments for Create Storage Pool into a config.

    Args:
      name: the name of the Storage Pool
      service_level: the service level of the Storage Pool
      capacity: the storage capacity of the Storage Pool
      description: the description of the Storage Pool
      labels: the parsed labels value

    Returns:
      The configuration that will be used as the request body for creating a
      Cloud NetApp Storage Pool.
    """
    storage_pool = self.messages.StoragePool()
    storage_pool.name = name
    storage_pool.serviceLevel = service_level
    storage_pool.capacityGib = capacity
    storage_pool.description = description
    storage_pool.labels = labels
    return storage_pool

  def ListStoragePools(self, location_ref, limit=None):
    """Make API calls to List active Cloud NetApp Storage Pools.

    Args:
      location_ref: The parsed location of the listed NetApp Volumes.
      limit: The number of Cloud NetApp Storage Pools to limit the results to.
        This limit is passed to the server and the server does the limiting.

    Returns:
      Generator that yields the Cloud NetApp Volumes.
    """
    request = self.messages.NetappProjectsLocationsStoragePoolsListRequest(
        parent=location_ref)
    # Check for unreachable locations.
    response = self.client.projects_locations_storagePools.List(request)
    for location in response.unreachable:
      log.warning('Location {} may be unreachable.'.format(location))
    return list_pager.YieldFromList(
        self.client.projects_locations_storagePools,
        request,
        field=STORAGE_POOL_RESOURCE,
        limit=limit,
        batch_size_attribute='pageSize')

  def GetStoragePool(self, storagepool_ref):
    """Get Cloud NetApp Storage Pool information."""
    request = self.messages.NetappProjectsLocationsStoragePoolsGetRequest(
        name=storagepool_ref.RelativeName())
    return self.client.projects_locations_storagePools.Get(request)

  def DeleteStoragePool(self, storagepool_ref, async_):
    """Deletes an existing Cloud NetApp Storage Pool."""
    request = self.messages.NetappProjectsLocationsStoragePoolsDeleteRequest(
        name=storagepool_ref.RelativeName())
    return self._DeleteStoragePool(async_, request)

  def _DeleteStoragePool(self, async_, request):
    delete_op = self.client.projects_locations_storagePools.Delete(request)
    if async_:
      return delete_op
    operation_ref = resources.REGISTRY.ParseRelativeName(
        delete_op.name, collection=OPERATIONS_COLLECTION)
    return self.WaitForOperation(operation_ref)

  def ParseUpdatedStoragePoolConfig(self,
                                    storagepool_config,
                                    capacity=None,
                                    description=None,
                                    labels=None):
    """Parses updates into a storage pool config.

    Args:
      storagepool_config: The storage pool message to update.
      capacity: capacity of a storage pool
      description: str, a new description, if any.
      labels: LabelsValue message, the new labels value, if any.

    Returns:
      The storage pool message.
    """
    storage_pool = self._adapter.ParseUpdatedStoragePoolConfig(
        storagepool_config,
        capacity=capacity,
        description=description,
        labels=labels)
    return storage_pool

  def UpdateStoragePool(self, storagepool_ref, storagepool_config, update_mask,
                        async_):
    """Updates a Storage Pool.

    Args:
      storagepool_ref: the reference to the storage pool.
      storagepool_config: Storage Pool message, the updated storage pool.
      update_mask: str, a comma-separated list of updated fields.
      async_: bool, if False, wait for the operation to complete.

    Returns:
      an Operation or Storage Pool message.
    """
    update_op = self._adapter.UpdateStoragePool(storagepool_ref,
                                                storagepool_config, update_mask)
    if async_:
      return update_op
    operation_ref = resources.REGISTRY.ParseRelativeName(
        update_op.name, collection=OPERATIONS_COLLECTION)
    return self.WaitForOperation(operation_ref)


class AlphaStoragePoolsAdapter(object):
  """Adapter for the Alpha Cloud NetApp Files API for Active Directories."""

  def __init__(self):
    self.release_track = base.ReleaseTrack.ALPHA
    self.client = GetClientInstance(release_track=self.release_track)
    self.messages = GetMessagesModule(release_track=self.release_track)

  def ParseUpdatedStoragePoolConfig(self,
                                    storagepool_config,
                                    description=None,
                                    labels=None,
                                    capacity=None):
    """Parse update information into an updated Storage Pool message."""
    if capacity is not None:
      storagepool_config.capacityGib = capacity
    if description is not None:
      storagepool_config.description = description
    if labels is not None:
      storagepool_config.labels = labels
    return storagepool_config

  def UpdateStoragePool(self, storagepool_ref, storagepool_config, update_mask):
    """Send a Patch request for the Cloud NetApp Storage Pool."""
    update_request = self.messages.NetappProjectsLocationsStoragePoolsPatchRequest(
        storagePool=storagepool_config,
        name=storagepool_ref.RelativeName(),
        updateMask=update_mask)
    update_op = self.client.projects_locations_storagePools.Patch(
        update_request)
    return update_op
