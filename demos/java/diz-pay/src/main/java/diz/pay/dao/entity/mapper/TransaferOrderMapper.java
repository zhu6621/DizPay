package diz.pay.dao.entity.mapper;

import diz.pay.dao.entity.domain.TransaferOrder;
import diz.pay.dao.entity.domain.TransaferOrderExample;
import org.apache.ibatis.annotations.Param;

import java.util.List;

public interface TransaferOrderMapper {
    long countByExample(TransaferOrderExample example);

    int deleteByExample(TransaferOrderExample example);

    int deleteByPrimaryKey(Integer id);

    int insert(TransaferOrder record);

    int insertSelective(TransaferOrder record);

    List<TransaferOrder> selectByExample(TransaferOrderExample example);

    TransaferOrder selectByPrimaryKey(Integer id);

    int updateByExampleSelective(@Param("record") TransaferOrder record, @Param("example") TransaferOrderExample example);

    int updateByExample(@Param("record") TransaferOrder record, @Param("example") TransaferOrderExample example);

    int updateByPrimaryKeySelective(TransaferOrder record);

    int updateByPrimaryKey(TransaferOrder record);
}