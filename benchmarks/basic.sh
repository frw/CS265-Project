../rocksdb/db_bench --use_existing_db=0 --num=524288000 --threads=1 --num_levels=6 --max_background_compactions=1 --max_background_flushes=1 --write_buffer_size=67108864 --max_write_buffer_number=3 --level0_stop_writes_trigger=12 --level0_slowdown_writes_trigger=20  --hard_pending_compaction_bytes_limit=137438953472 --soft_pending_compaction_bytes_limit=137438953476 --max_bytes_for_level_base=134217728 --max_bytes_for_level_multiplier=8 --target_file_size_base=67108864 --target_file_size_multiplier=1 --statistics=1 --stats_per_interval=600 --benchmarks=fillrandom 

#--write_buffer_size=134217728 --target_file_size_base=134217728
#--max_bytes_for_level_base=1073741824 --target_file_size_base=67108864
