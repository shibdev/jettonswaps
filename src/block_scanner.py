from collections import deque
from pytoniq_core.tlb.block import ExtBlkRef
from pytoniq.liteclient import LiteClient
from pytoniq_core.tl import BlockIdExt
from pytoniq_core.tlb import Block
from pytoniq_core.tlb.block import BlkPrevInfo

import typing


class BlocksScanner:
    def __init__(self, client: LiteClient, block_handler: typing.Callable[[BlockIdExt], typing.Coroutine]):
        self.client = client
        self.block_handler = block_handler
        self.shards_storage: dict[str, int] = {}
        self.blks_dequeue = deque()
        self.is_initialized = False

    async def run(self) -> None:
        if not self.client.inited:
            raise Exception("LiteClient must be initialized")

        master_blk: BlockIdExt = self._mc_info_to_tl_blk(
            await self.client.get_masterchain_info()
        )

        if not self.is_initialized:
            shards: list[BlockIdExt] = await self.client.get_all_shards_info(master_blk)

            for shard in shards:
                self.shards_storage[self._get_shard_id(shard)] = shard.seqno
                self.blks_dequeue.append(shard)

            self.is_initialized = True

        while True:
            self.blks_dequeue.append(master_blk)

            shards: list[BlockIdExt] = await self.client.get_all_shards_info(master_blk)

            for shard in shards:
                await self.parse_not_seen_shards(shard)

                self.shards_storage[self._get_shard_id(shard)] = shard.seqno

            while self.blks_dequeue:
                await self.block_handler(self.client, self.blks_dequeue.pop())

            last_seqno: int = master_blk.seqno

            while True:
                new_master_blk: BlockIdExt = self._mc_info_to_tl_blk(
                    await self.client.get_masterchain_info_ext()
                )

                if new_master_blk.seqno != last_seqno:
                    master_blk = new_master_blk
                    break

    async def parse_not_seen_shards(self, shard: BlockIdExt):
        if self.shards_storage.get(self._get_shard_id(shard)) == shard.seqno:
            return

        self.blks_dequeue.append(shard)
        full_blk: Block = await self.client.raw_get_block_header(shard)
        prev_ref: BlkPrevInfo = full_blk.info.prev_ref

        if prev_ref.type_ == "prev_blk_info":
            prev: ExtBlkRef = prev_ref.prev

            await self.parse_not_seen_shards(
                BlockIdExt(
                    workchain = shard.workchain,
                    seqno = prev.seqno,
                    shard = shard.shard,
                    root_hash = prev.root_hash,
                    file_hash = prev.file_hash
                )
            )

        else:
            prev1: ExtBlkRef = prev_ref.prev1
            prev2: ExtBlkRef = prev_ref.prev2

            await self.parse_not_seen_shards(
                BlockIdExt(
                    workchain = shard.workchain,
                    seqno = prev1.seqno,
                    shard = shard.shard,
                    root_hash = prev1.root_hash,
                    file_hash = prev1.file_hash
                )
            )

            await self.parse_not_seen_shards(
                BlockIdExt(
                    workchain = shard.workchain,
                    seqno = prev2.seqno,
                    shard = shard.shard,
                    root_hash = prev2.root_hash,
                    file_hash = prev2.file_hash
                )
            )

    @staticmethod
    def _mc_info_to_tl_blk(info: dict) -> BlockIdExt:
        return BlockIdExt.from_dict(info["last"])

    @staticmethod
    def _get_shard_id(blk: BlockIdExt) -> str:
        return "{}:{}".format(
            blk.workchain,
            blk.shard
        )
