package socialposts.pipeline.sources;

public interface SocialSource {
  SocialQueryResult search(SocialQuery query) throws Exception;

  void setOAuthConsumer(String key, String secret);

  void setOAuthAccessToken(String accessToken, String tokenSecret);
}
