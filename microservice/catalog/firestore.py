# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START bookshelf_firestore_client_import]
from google.cloud import firestore
# [END bookshelf_firestore_client_import]


def next_page(limit=10, start_after=None):
    db = firestore.Client()

    query = db.collection(u'Product').limit(limit).order_by(u'price')

    if start_after:
        # Construct a new query starting at this document.
        query = query.start_after({u'id': start_after})

    docs = query.stream()
    docs = list(map(document_to_dict, docs))

    last_item_id = None
    if limit == len(docs):
        # Get the last document from the results and set as the last sku id.
        last_item_id = docs[-1][u'id']
    return docs, last_item_id
