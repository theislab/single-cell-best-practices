#!/bin/bash
mkdir container
scp vicb-submit-01:/storage/groups/ml01/workspace/ml_charliecloud_containers/best_practice_book/211119/sc_best_practice_book_211119.dockerimg .
mv sc_best_practice_book_211119.dockerimg container
docker load -i container/sc_best_practice_book_211119.dockerimg
