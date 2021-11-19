# Allow classes to use self-referencing Type hints in Python 3.7.
from __future__ import annotations

import pyarrow as pa

from deltacat.storage import Locator, NamespaceLocator, TableLocator
from deltacat.types.media import ContentType
from typing import Any, Dict, List, Optional, Union


class TableVersion(dict):
    @staticmethod
    def of(table_version_locator: Optional[TableVersionLocator],
           schema: Optional[Union[pa.Schema, str, bytes]],
           partition_keys: Optional[List[Dict[str, Any]]] = None,
           primary_key_column_names: Optional[List[str]] = None,
           table_version_description: Optional[str] = None,
           table_version_properties: Optional[Dict[str, str]] = None,
           supported_content_types: Optional[List[ContentType]] = None) \
            -> TableVersion:
        return TableVersion({
            "tableVersionLocator": table_version_locator,
            "schema": schema,
            "partitionKeys": partition_keys,
            "primaryKeys": primary_key_column_names,
            "description": table_version_description,
            "properties": table_version_properties,
            "contentTypes": supported_content_types,
        })

    @property
    def table_version_locator(self) -> Optional[TableVersionLocator]:
        return self.get("tableVersionLocator")

    @table_version_locator.setter
    def table_version_locator(
            self,
            table_version_locator: Optional[TableVersionLocator]) -> None:
        self["tableVersionLocator"] = table_version_locator

    @property
    def schema(self) -> Optional[Union[pa.Schema, str, bytes]]:
        return self.get("schema")

    @schema.setter
    def schema(self, schema: Optional[Union[pa.Schema, str, bytes]]) -> None:
        self["schema"] = schema

    @property
    def partition_keys(self) -> Optional[List[Dict[str, Any]]]:
        return self.get("partitionKeys")

    @partition_keys.setter
    def partition_keys(
            self,
            partition_keys: Optional[List[Dict[str, Any]]]) -> None:
        self["partitionKeys"] = partition_keys

    @property
    def primary_keys(self) -> Optional[List[str]]:
        return self.get("primaryKeys")

    @primary_keys.setter
    def primary_keys(self, primary_keys: Optional[List[str]]) -> None:
        self["primaryKeys"] = primary_keys

    @property
    def description(self) -> Optional[str]:
        return self.get("description")

    @description.setter
    def description(self, description: Optional[str]) -> None:
        self["description"] = description

    @property
    def properties(self) -> Optional[Dict[str, str]]:
        return self.get("properties")

    @properties.setter
    def properties(self, properties: Optional[Dict[str, str]]) -> None:
        self["properties"] = properties

    @property
    def content_types(self) -> Optional[List[ContentType]]:
        content_types = self.get("contentTypes")
        return None if content_types is None else \
            [None if _ is None else ContentType(_) for _ in content_types]

    @content_types.setter
    def content_types(
            self,
            content_types: Optional[List[ContentType]]) -> None:
        self["contentTypes"] = content_types

    @property
    def namespace_locator(self) -> Optional[NamespaceLocator]:
        table_version_locator = self.table_version_locator
        if table_version_locator:
            return table_version_locator.namespace_locator
        return None

    @property
    def table_locator(self) -> Optional[TableLocator]:
        table_version_locator = self.table_version_locator
        if table_version_locator:
            return table_version_locator.table_locator
        return None

    @property
    def namespace(self) -> Optional[str]:
        table_version_locator = self.table_version_locator
        if table_version_locator:
            return table_version_locator.namespace
        return None

    @property
    def table_name(self) -> Optional[str]:
        table_version_locator = self.table_version_locator
        if table_version_locator:
            return table_version_locator.table_name
        return None

    @property
    def table_version(self) -> Optional[str]:
        table_version_locator = self.table_version_locator
        if table_version_locator:
            return table_version_locator.table_version
        return None

    def is_supported_content_type(
            self,
            content_type: ContentType):
        supported_content_types = self.content_types
        return (not supported_content_types) or \
               (content_type in supported_content_types)


class TableVersionLocator(Locator, dict):
    @staticmethod
    def of(table_locator: Optional[TableLocator],
           table_version: Optional[str]) -> TableVersionLocator:
        return TableVersionLocator({
            "tableLocator": table_locator,
            "tableVersion": table_version,
        })

    @property
    def table_locator(self) -> Optional[TableLocator]:
        return self.get("tableLocator")

    @table_locator.setter
    def table_locator(self, table_locator: Optional[TableLocator]) -> None:
        self["tableLocator"] = table_locator

    @property
    def table_version(self) -> Optional[str]:
        return self.get("tableVersion")

    @table_version.setter
    def table_version(self, table_version: Optional[str]) -> None:
        self["tableVersion"] = table_version

    @property
    def namespace_locator(self) -> Optional[NamespaceLocator]:
        table_locator = self.table_locator
        if table_locator:
            return table_locator.namespace_locator
        return None

    @property
    def namespace(self) -> Optional[str]:
        table_locator = self.table_locator
        if table_locator:
            return table_locator.namespace
        return None

    @property
    def table_name(self) -> Optional[str]:
        table_locator = self.table_locator
        if table_locator:
            return table_locator.table_name
        return None

    def canonical_string(self) -> str:
        """
        Returns a unique string for the given locator that can be used
        for equality checks (i.e. two locators are equal if they have
        the same canonical string).
        """
        tl_hexdigest = self.table_locator.hexdigest()
        table_version = self.table_version
        return f"{tl_hexdigest}|{table_version}"
