SOURCES=db/builder.cc db/c.cc db/compaction.cc db/compaction_picker.cc db/db_filesnapshot.cc db/db_impl.cc db/db_impl_readonly.cc db/db_iter.cc db/db_stats_logger.cc db/dbformat.cc db/filename.cc db/internal_stats.cc db/log_reader.cc db/log_writer.cc db/memtable.cc db/memtable_list.cc db/merge_helper.cc db/merge_operator.cc db/repair.cc db/table_cache.cc db/table_properties_collector.cc db/tailing_iter.cc db/transaction_log_impl.cc db/version_edit.cc db/version_set.cc db/write_batch.cc table/block.cc table/block_based_table_builder.cc table/block_based_table_factory.cc table/block_based_table_reader.cc table/block_builder.cc table/block_hash_index.cc table/filter_block.cc table/flush_block_policy.cc table/format.cc table/iterator.cc table/merger.cc table/meta_blocks.cc table/plain_table_builder.cc table/plain_table_factory.cc table/plain_table_reader.cc table/table_properties.cc table/two_level_iterator.cc util/arena.cc util/auto_roll_logger.cc util/blob_store.cc util/bloom.cc util/build_version.cc util/cache.cc util/coding.cc util/comparator.cc util/crc32c.cc util/dynamic_bloom.cc util/env.cc util/env_hdfs.cc util/env_posix.cc util/filter_policy.cc util/hash.cc util/hash_linklist_rep.cc util/hash_skiplist_rep.cc util/histogram.cc util/ldb_cmd.cc util/ldb_tool.cc util/log_buffer.cc util/logging.cc util/murmurhash.cc util/options.cc util/perf_context.cc util/skiplistrep.cc util/slice.cc util/statistics.cc util/status.cc util/string_util.cc util/sync_point.cc util/thread_local.cc util/vectorrep.cc utilities/backupable/backupable_db.cc utilities/geodb/geodb_impl.cc utilities/merge_operators/put.cc utilities/merge_operators/string_append/stringappend.cc utilities/merge_operators/string_append/stringappend2.cc utilities/merge_operators/uint64add.cc utilities/redis/redis_lists.cc utilities/ttl/db_ttl.cc  port/port_posix.cc port/stack_trace.cc  
SOURCESCPP=
MEMENV_SOURCES=helpers/memenv/memenv.cc
CC=cc
CXX=g++
PLATFORM=OS_MACOSX
PLATFORM_LDFLAGS= -lsnappy -lgflags -lz -lbz2 -llz4
VALGRIND_VER=
PLATFORM_CCFLAGS= -DROCKSDB_PLATFORM_POSIX  -DOS_MACOSX -DROCKSDB_ATOMIC_PRESENT -DSNAPPY -DGFLAGS -DZLIB -DBZIP2 -DLZ4 
PLATFORM_CXXFLAGS=-std=c++11  -DROCKSDB_PLATFORM_POSIX  -DOS_MACOSX -DROCKSDB_ATOMIC_PRESENT -DSNAPPY -DGFLAGS -DZLIB -DBZIP2 -DLZ4 
PLATFORM_SHARED_CFLAGS=-fPIC
PLATFORM_SHARED_EXT=dylib
PLATFORM_SHARED_LDFLAGS=-dynamiclib -install_name 
PLATFORM_SHARED_VERSIONED=false
EXEC_LDFLAGS=
JEMALLOC_INCLUDE=
JEMALLOC_LIB=
