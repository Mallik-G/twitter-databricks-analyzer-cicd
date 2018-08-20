package social.pipeline.custom;

import org.junit.Assert;
import org.junit.Test;
import socialposts.pipeline.sources.SocialMessage;
import socialposts.pipeline.sources.SocialQuery;
import socialposts.pipeline.sources.SocialQueryResult;

import java.util.ArrayList;
import java.util.List;

public class PredefinedSourceTest {

  @Test
  public void test_customSource() throws Exception {
    PredefinedSource source = new PredefinedSource("/test_messages.json");
    SocialQueryResult my_query = source.search(new SocialQuery("my query"));
    SocialMessage socialMessage = my_query.getMessages().get(0);

    Assert.assertEquals(socialMessage.getText(),"Hello");

  }

}
