from unittest.mock import AsyncMock, patch
import pytest
from app.services.crypto_service import wallet_info


@pytest.mark.asyncio
async def test_wallet_info_write_to_db():
    wallet_address = "THogKGBqyQdkV77u8J51x4J3MbxWsZNzxu"

    with patch("app.core.tron.tron.get_account") as mock_get_account, \
         patch("app.core.tron.tron.get_bandwidth") as mock_get_bandwidth:

        mock_get_account.return_value = {"balance": 10_000_000, "energy": 2000}
        mock_get_bandwidth.return_value = 1500

        session = AsyncMock()
        result = await wallet_info(wallet_address, get_db=session)

        assert result.bandwidth == 1500
        assert result.energy == 2000
        assert result.balance == 10.0

        mock_get_account.assert_called_once_with(wallet_address)
        mock_get_bandwidth.assert_called_once_with(wallet_address)
        session.add.assert_called_once()
        session.commit.assert_called_once()
        session.refresh.assert_called_once()
